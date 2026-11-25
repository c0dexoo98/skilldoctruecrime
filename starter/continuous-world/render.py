#!/usr/bin/env python3
"""Deterministically render a continuous code-authored world to H.264 MP4."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import subprocess
import time
from pathlib import Path
from typing import Any
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


def ffprobe_duration(path: Path) -> float:
    result = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)
    ], text=True)
    return float(result.strip())


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def hermite_path(points: list[dict[str, Any]], t: float, dimensions: int) -> tuple[float, ...]:
    """Cubic Hermite interpolation with time-domain tangents shared at knots (C1)."""
    times = [float(p["at"]) for p in points]
    vals = [tuple(float(v) for v in p["value"]) for p in points]
    if t <= times[0]:
        return vals[0]
    if t >= times[-1]:
        return vals[-1]
    i = next(j for j in range(len(times) - 1) if times[j] <= t <= times[j + 1])
    t0, t1 = times[i], times[i + 1]
    dt = t1 - t0
    u = (t - t0) / dt
    def tangent(j: int, k: int) -> float:
        if j == 0:
            return (vals[1][k] - vals[0][k]) / (times[1] - times[0])
        if j == len(times) - 1:
            return (vals[-1][k] - vals[-2][k]) / (times[-1] - times[-2])
        return (vals[j + 1][k] - vals[j - 1][k]) / (times[j + 1] - times[j - 1])
    h00, h10 = 2*u**3 - 3*u**2 + 1, u**3 - 2*u**2 + u
    h01, h11 = -2*u**3 + 3*u**2, u**3 - u**2
    out = []
    for k in range(dimensions):
        out.append(h00*vals[i][k] + h10*dt*tangent(i,k) + h01*vals[i+1][k] + h11*dt*tangent(i+1,k))
    return tuple(out)


def active_beat(beats: list[dict[str, Any]], t: float) -> dict[str, Any]:
    chosen = beats[0]
    for beat in beats:
        if float(beat["start"]) <= t:
            chosen = beat
        else:
            break
    return chosen


def get_font(size: int, font_path: str | None = None, language: str = "en") -> ImageFont.ImageFont:
    rtl = language.lower().split("-")[0] in {"fa", "ar", "ur", "he"}
    latin = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"]
    arabic = ["/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    candidates = [font_path, *(arabic if rtl else latin)]
    for item in candidates:
        if item and Path(item).is_file():
            try:
                return ImageFont.truetype(item, size, layout_engine=ImageFont.Layout.RAQM)
            except Exception:
                try:
                    return ImageFont.truetype(item, size)
                except Exception:
                    pass
    return ImageFont.load_default()


def fit_image(source: Image.Image, width: int, height: int) -> Image.Image:
    return ImageOps.contain(source.convert("RGB"), (max(1,width), max(1,height)), Image.Resampling.LANCZOS)


def world_to_screen(x: float, y: float, cam: tuple[float,...], w: int, h: int) -> tuple[float,float]:
    cx,cy,zoom,rotation=cam
    dx=float(x)-cx; dy=(float(y)-cy)*.72
    angle=math.radians(-rotation); co,si=math.cos(angle),math.sin(angle)
    rx=dx*co-dy*si; ry=dx*si+dy*co
    return w/2+rx*zoom,h*.55+ry*zoom


def photo_card(obj: dict[str, Any], scale: float, rotation: float, asset_cache: dict[str, Image.Image]) -> Image.Image:
    image_path = str(obj["image"])
    if image_path not in asset_cache:
        asset_cache[image_path] = Image.open(image_path).convert("RGB")
    source = asset_cache[image_path]
    sw, sh = obj.get("size", [420, 300])
    cw, ch = max(24, int(sw*scale)), max(24, int(sh*scale))
    margin = max(8, int(min(cw,ch)*0.045))
    card = Image.new("RGBA", (cw, ch), tuple(obj.get("paper_color", [236, 227, 205])) + (255,))
    fitted = fit_image(source, cw-2*margin, ch-2*margin)
    px, py = (cw-fitted.width)//2, (ch-fitted.height)//2
    card.paste(fitted, (px, py))
    if obj.get("show_label") and obj.get("label"):
        draw = ImageDraw.Draw(card)
        language=obj.get("language","en"); direction="rtl" if language.lower().split("-")[0] in {"fa","ar","ur","he"} else "ltr"
        font = get_font(max(10, int(ch*0.055)), obj.get("font"), language)
        draw.text((margin, ch-margin), str(obj["label"]), fill=(75,72,64,255), font=font, anchor="ls", direction=direction, language=language)
    return card.rotate(-rotation, resample=Image.Resampling.BICUBIC, expand=True)


def route_segment(points: list[list[float]], progress: float) -> list[tuple[float,float]]:
    if not points or progress <= 0:
        return []
    pts = [(float(p[0]),float(p[1])) for p in points]
    lengths = [math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)]
    total = sum(lengths)
    if total <= 0:
        return pts[:1]
    remaining = max(0.0,min(1.0,progress))*total
    result=[pts[0]]
    for i,length in enumerate(lengths):
        if remaining >= length:
            result.append(pts[i+1]); remaining -= length
        else:
            if length:
                q=remaining/length; a,b=pts[i],pts[i+1]
                result.append((a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q))
            break
    return result


def object_position(obj: dict[str, Any], t: float) -> tuple[float,float,float]:
    frames = sorted(obj.get("motion", []), key=lambda k: float(k["at"]))
    if not frames:
        if "pos" in obj:
            x,y=obj["pos"]
        elif obj.get("shape")=="route" and obj.get("points"):
            points=obj["points"]; x=sum(float(p[0]) for p in points)/len(points); y=sum(float(p[1]) for p in points)/len(points)
        else:
            raise ValueError(f"Object {obj.get('id','<unknown>')} needs a pos [x,y] or motion path")
        return float(x),float(y),float(obj.get("rotation",0))
    vals=[{"at":float(k["at"]),"value":[float(k["pos"][0]),float(k["pos"][1]),float(k.get("rotation",obj.get("rotation",0)))]} for k in frames]
    x,y,rot=hermite_path(vals,t,3)
    return x,y,rot


def draw_background(w: int, h: int, cam: tuple[float,...], cfg: dict[str,Any]) -> Image.Image:
    # A stable, code-drawn desk/world; its coordinate grid stays anchored to the camera path.
    base = Image.new("RGB",(w,h),(16,25,34)); d=ImageDraw.Draw(base)
    horizon=int(h*0.10)
    for y in range(horizon,h):
        q=(y-horizon)/max(1,h-horizon)
        col=(int(29+20*q),int(44+20*q),int(54+17*q))
        d.line((0,y,w,y),fill=col)
    cx,cy,zoom,rotation=cam
    zoom=max(.08,min(8.0,zoom))
    # World-anchored grid; rotate/scale with the same camera transform as every prop.
    span_x=w/zoom+700; span_y=h/(zoom*.72)+700; step=max(110.0,220.0/zoom)
    gx0=math.floor((cx-span_x/2)/step)*step; gx1=cx+span_x/2
    gy0=math.floor((cy-span_y/2)/step)*step; gy1=cy+span_y/2
    x=gx0
    while x<=gx1:
        d.line([world_to_screen(x,cy-span_y/2,cam,w,h),world_to_screen(x,cy+span_y/2,cam,w,h)],fill=(61,76,78),width=1); x+=step
    y=gy0
    while y<=gy1:
        d.line([world_to_screen(cx-span_x/2,y,cam,w,h),world_to_screen(cx+span_x/2,y,cam,w,h)],fill=(61,76,78),width=1); y+=step
    # Broad code-drawn practical-light pool.
    glow=Image.new("RGBA",(w,h),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse((w*.17,-h*.38,w*.95,h*.96),fill=(231,184,113,28))
    glow=glow.filter(ImageFilter.GaussianBlur(max(12,int(min(w,h)*.14))))
    return Image.alpha_composite(base.convert("RGBA"),glow).convert("RGB")


def draw_object(canvas: Image.Image, obj: dict[str,Any], cam: tuple[float,...], t: float,
                hero: bool, cache: dict[str,Image.Image]) -> None:
    w,h=canvas.size; cx,cy,zoom,camrot=cam; zoom=max(.08,min(8.0,zoom))
    ox,oy,object_rot=object_position(obj,t)
    sx,sy=world_to_screen(ox,oy,cam,w,h)
    dim_alpha=1.0 if hero else float(obj.get("secondary_alpha",.24))
    if "image" in obj:
        path=Path(obj["image"])
        source=str(path)
        card=photo_card(obj,zoom,object_rot-camrot,cache)
        shadow=Image.new("RGBA",card.size,(0,0,0,0)); shadow.putalpha(card.getchannel("A"))
        shadow=Image.new("RGBA",card.size,(4,8,11,0)); shadow.putalpha(card.getchannel("A").point(lambda a:int(a*.48)))
        shadow=shadow.filter(ImageFilter.GaussianBlur(max(2,int(10*zoom))))
        left=int(sx-card.width/2); top=int(sy-card.height/2)
        layer=Image.new("RGBA",canvas.size,(0,0,0,0)); layer.alpha_composite(shadow,(left+int(8*zoom),top+int(12*zoom)))
        layer.alpha_composite(card,(left,top))
        if dim_alpha<1:
            layer.putalpha(layer.getchannel("A").point(lambda a:int(a*dim_alpha)))
        canvas.alpha_composite(layer)
        return
    shape=obj.get("shape","circle"); size=obj.get("size",[70,70])
    if isinstance(size,(int,float)): rw=rh=float(size)
    else: rw,rh=float(size[0]),float(size[1])
    rw=max(2,int(rw*zoom)); rh=max(2,int(rh*zoom))
    color=tuple(obj.get("color",[157,99,68])); alpha=int(255*dim_alpha)
    pad=max(12,int(max(rw,rh)*.65)); local=Image.new("RGBA",(rw+pad*2,rh+pad*2),(0,0,0,0)); d=ImageDraw.Draw(local)
    mx,my=local.width/2,local.height/2; box=(int(mx-rw/2),int(my-rh/2),int(mx+rw/2),int(my+rh/2))
    if shape=="circle": d.ellipse(box,fill=color+(alpha,),outline=(235,225,204,alpha),width=max(2,int(3*zoom)))
    elif shape=="box": d.rounded_rectangle(box,radius=max(3,int(8*zoom)),fill=color+(alpha,),outline=(235,225,204,alpha),width=max(2,int(3*zoom)))
    elif shape=="pin":
        r=max(5,rw//3); d.ellipse((int(mx-r),int(my-r),int(mx+r),int(my+r)),fill=(190,38,36,alpha),outline=(246,226,197,alpha),width=max(2,int(3*zoom))); d.polygon([(mx-r*.55,my+r*.55),(mx+r*.55,my+r*.55),(mx,my+r*2.2)],fill=(190,38,36,alpha))
    elif shape=="route": return
    else: raise ValueError(f"Unsupported shape: {shape}")
    local=local.rotate(-(object_rot-camrot),resample=Image.Resampling.BICUBIC,expand=True)
    canvas.alpha_composite(local,(int(sx-local.width/2),int(sy-local.height/2)))


def draw_routes(canvas: Image.Image, objects: list[dict[str,Any]], cam: tuple[float,...], t: float, hero_id: str) -> None:
    w,h=canvas.size; cx,cy,zoom,_=cam; d=ImageDraw.Draw(canvas)
    for obj in objects:
        if obj.get("shape")!="route": continue
        reveal=obj.get("reveal",{})
        start=float(reveal.get("start",0)); end=float(reveal.get("end",start+1))
        q=smoothstep((t-start)/max(.001,end-start))
        pts=route_segment(obj.get("points",[]),q)
        if len(pts)<2: continue
        screen=[world_to_screen(x,y,cam,w,h) for x,y in pts]
        a=1.0 if obj["id"]==hero_id else float(obj.get("secondary_alpha",.24))
        color=tuple(obj.get("color",[190,38,36])); col=tuple(int(c*a) for c in color)
        width=max(2,int(float(obj.get("line_width",6))*zoom))
        d.line(screen,fill=col,width=width,joint="curve")
        if q>0.98:
            x,y=screen[-1]; r=max(3,width*1.35); d.ellipse((x-r,y-r,x+r,y+r),fill=col)


def draw_text(canvas: Image.Image, beat: dict[str,Any], objects: list[dict[str,Any]], cam: tuple[float,...], cfg: dict[str,Any], t: float) -> None:
    block=beat.get("text") or {}; value=str(block.get("value","")).strip()
    channel=block.get("channel","none")
    if not value or channel=="none": return
    language=cfg.get("language","en"); direction="rtl" if language.lower().split("-")[0] in {"fa","ar","ur","he"} else "ltr"
    font=get_font(int(cfg.get("text_size", max(32,canvas.height*.055))),cfg.get("font"),language)
    d=ImageDraw.Draw(canvas,"RGBA")
    if channel=="overlay":
        box=d.textbbox((0,0),value,font=font,direction=direction,language=language); tw,th=box[2]-box[0],box[3]-box[1]
        x=(canvas.width-tw)//2; y=int(canvas.height*.12)
        d.rounded_rectangle((x-20,y-12,x+tw+20,y+th+12),radius=12,fill=(8,12,16,220))
        d.text((x,y),value,font=font,fill=(249,243,229,255),direction=direction,language=language)
    elif channel=="document":
        target=block.get("object_id")
        obj=next((o for o in objects if o["id"]==target),None)
        if not obj or "image" in obj: raise ValueError("Document text needs a code-drawn paper object; do not bake duplicate text into a photo.")
        x,y,_=object_position(obj,t); sx,sy=world_to_screen(x,y,cam,canvas.width,canvas.height)
        d.text((sx,sy),value,font=font,fill=(48,45,39,255),anchor="mm",direction=direction,language=language)
    else:
        raise ValueError("text.channel must be none, overlay, or document; each phrase has only one visible channel")


def apply_finish(frame: Image.Image, cfg: dict[str,Any], t: float) -> Image.Image:
    fx=cfg.get("effects",{})
    if fx.get("glow",False):
        blurred=frame.filter(ImageFilter.GaussianBlur(max(2,int(min(frame.size)*.012))))
        frame=Image.blend(frame,blurred,.075)
    if fx.get("vignette",True):
        w,h=frame.size; mask=Image.new("L",(w,h),0); d=ImageDraw.Draw(mask)
        d.ellipse((-w*.17,-h*.2,w*1.17,h*1.2),fill=230)
        mask=mask.filter(ImageFilter.GaussianBlur(int(min(w,h)*.15)))
        frame=Image.composite(frame,Image.new("RGB",(w,h),(4,8,12)),mask)
    if fx.get("grain",True):
        rng=np.random.default_rng(int(t*cfg["fps"])+int(cfg.get("seed",19)))
        values=np.clip(rng.normal(128,22,(frame.height,frame.width)),0,255).astype(np.uint8)
        noise=Image.fromarray(values,"L").convert("RGB")
        frame=Image.blend(frame,noise,float(fx.get("grain_strength",.025)))
    return frame


def resolve_path(base: Path, value: str | None) -> Path | None:
    if not value: return None
    path=Path(value)
    return path.resolve() if path.is_absolute() else (base/path).resolve()


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project",help="project JSON")
    ap.add_argument("-o","--output",help="output MP4 override")
    ap.add_argument("--provenance",help="manifest JSON override")
    ap.add_argument("--dry-run",action="store_true",help="validate and print manifest without rendering")
    args=ap.parse_args()
    config_path=Path(args.project).resolve(); cfg=json.loads(config_path.read_text(encoding="utf-8")); base=config_path.parent
    w,h,fps=int(cfg["width"]),int(cfg["height"]),int(cfg["fps"]); duration=float(cfg["duration"])
    if w<64 or h<64 or fps<1 or duration<=0: raise ValueError("width/height >=64, fps >=1, and duration >0 are required")
    beats=sorted(cfg["beats"],key=lambda b:float(b["start"]))
    if not beats or abs(float(beats[0]["start"]))>1e-6: raise ValueError("beats must start at time 0")
    visible_phrases=[]
    for i,b in enumerate(beats):
        if "end" not in b: raise ValueError("every beat needs an explicit end time")
        start=float(b["start"]); end=float(b["end"])
        if not (0<=start<end<=duration+1e-6): raise ValueError("each beat needs 0 <= start < end <= duration")
        if i and abs(start-float(beats[i-1]["end"]))>1e-4: raise ValueError("beats must be contiguous: no gaps or overlaps")
        if i==len(beats)-1 and abs(end-duration)>1e-4: raise ValueError("the final beat must end at the configured duration")
        text=b.get("text",{}); channel=text.get("channel","none") if isinstance(text,dict) else "invalid"
        if channel not in {"none","overlay","document"}: raise ValueError("Each phrase must use exactly one text channel: none, overlay, or document")
        phrase=str(text.get("value","")).strip() if isinstance(text,dict) else ""
        if phrase:
            if phrase.casefold() in visible_phrases: raise ValueError("A visible phrase is repeated; keep one on-screen instance per phrase")
            visible_phrases.append(phrase.casefold())
    objects=cfg.get("objects",[]); ids=[o["id"] for o in objects]
    if len(ids)!=len(set(ids)): raise ValueError("object ids must be unique")
    for obj in objects:
        label=str(obj.get("label","")).strip()
        if obj.get("show_label") and label:
            if label.casefold() in visible_phrases: raise ValueError("A photo label duplicates a visible phrase; choose one screen channel")
            visible_phrases.append(label.casefold())
    for b in beats:
        if b["hero"] not in ids: raise ValueError(f"Unknown hero object: {b['hero']}")
    camera=sorted(cfg.get("camera_waypoints",[]),key=lambda p:float(p["at"]))
    if len(camera)<2: raise ValueError("At least two camera_waypoints are required for a continuous move")
    if float(camera[0]["at"])>0 or float(camera[-1]["at"])<duration: raise ValueError("camera_waypoints must cover 0 through the full duration")
    if any(float(camera[i]["at"])>=float(camera[i+1]["at"]) for i in range(len(camera)-1)): raise ValueError("camera waypoint times must be strictly increasing")
    for p in camera:
        if len(p["value"])!=4 or float(p["value"][2])<=0: raise ValueError("camera value is [world_x, world_y, zoom, rotation_degrees]")
    provenance=[]; asset_cache={}
    for obj in objects:
        if "image" in obj:
            path=resolve_path(base,str(obj["image"]))
            if not path or not path.is_file(): raise FileNotFoundError(path)
            obj["image"]=str(path); digest=hashlib.sha256(path.read_bytes()).hexdigest()
            meta=obj.get("provenance",{})
            provenance.append({"path":str(path),"sha256":digest,"source":meta.get("source","unverified"),"rights":meta.get("rights","unverified"),"status":meta.get("status","illustrative/unverified"),"beat_use":[b["start"] for b in beats if b["hero"]==obj["id"]]})
    voice=resolve_path(base,cfg.get("voiceover"))
    voice_duration=None
    if voice:
        if not voice.is_file(): raise FileNotFoundError(voice)
        voice_duration=ffprobe_duration(voice)
        tolerance=max(.04,.5/fps)
        if abs(voice_duration-duration)>tolerance:
            raise ValueError(f"Configured duration {duration:.6f}s differs from voice {voice_duration:.6f}s; use measured voice duration; do not trim or retime silently")
    output=resolve_path(base,args.output or cfg.get("output","continuous-world.mp4")); assert output
    manifest_path=resolve_path(base,args.provenance) if args.provenance else output.with_suffix(".provenance.json")
    n=round(duration*fps)
    manifest={"renderer":"continuous-world-code-renderer/2.0","input_json":str(config_path),"input_sha256":hashlib.sha256(config_path.read_bytes()).hexdigest(),"output":str(output),"format":"MP4/H.264","duration_seconds":duration,"frame_duration_seconds":n/fps,"fps":fps,"resolution":[w,h],"frames":n,"voiceover":str(voice) if voice else None,"voiceover_duration_seconds":voice_duration,"assets":provenance,"asset_policy":"Only project-declared user/permission-cleared photos may be composited as physical prints; no AI video, stock or downloaded video clips.","beats":beats,"camera_waypoints":camera,"created_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
    if args.dry_run:
        print(json.dumps(manifest,ensure_ascii=False,indent=2)); return
    output.parent.mkdir(parents=True,exist_ok=True); manifest_path.parent.mkdir(parents=True,exist_ok=True)
    command=["ffmpeg","-y","-hide_banner","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(fps),"-i","-"]
    if voice: command += ["-i",str(voice)]
    command += ["-map","0:v:0"]
    if voice: command += ["-map","1:a:0","-af","asetpts=PTS-STARTPTS","-c:a","aac","-b:a",str(cfg.get("audio_bitrate","192k")),"-ar","48000","-ac","2"]
    else: command += ["-an"]
    command += ["-t",f"{duration:.6f}","-c:v","libx264","-preset",cfg.get("preset","veryfast"),"-crf",str(cfg.get("crf",18)),"-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    prior_frame=None; previous_camera=None; cache={}; start_clock=time.time()
    try:
        for i in range(n):
            t=i/fps
            cx,cy,zoom,rotation=hermite_path(camera,t,4)
            drift=cfg.get("camera_drift",[.25,.08])
            cx+=float(drift[0])*t; cy+=float(drift[1])*t
            shake=float(cfg.get("handheld",0.0))
            if shake:
                cx+=shake*math.sin(t*2*math.pi*.42); cy+=shake*.65*math.sin(t*2*math.pi*.31+.4)
            cam=(cx,cy,zoom,rotation)
            beat=active_beat(beats,t)
            frame=draw_background(w,h,cam,cfg).convert("RGBA")
            for obj in objects:
                draw_object(frame,obj,cam,t,obj["id"]==beat["hero"],cache)
            draw_routes(frame,objects,cam,t,beat["hero"])
            draw_text(frame,beat,objects,cam,cfg,t)
            rgb=apply_finish(frame.convert("RGB"),cfg,t)
            if prior_frame is not None and previous_camera is not None:
                speed=(math.dist(cam[:2],previous_camera[:2])+abs(cam[2]-previous_camera[2])*300+abs(cam[3]-previous_camera[3])*3)*fps
                alpha=min(float(cfg.get("max_motion_blur",.22)),speed*float(cfg.get("motion_blur_strength",.00045)))
                if alpha>0.008: rgb=Image.blend(rgb,prior_frame,alpha)
            proc.stdin.write(rgb.tobytes()); prior_frame=rgb; previous_camera=cam
            if i and i%(fps*5)==0: print(f"rendered {i}/{n} frames ({t:.1f}s)",flush=True)
        proc.stdin.close()
        code=proc.wait()
        if code: raise subprocess.CalledProcessError(code,command)
    except Exception:
        if proc.poll() is None: proc.kill()
        raise
    manifest["output_bytes"]=output.stat().st_size
    manifest["elapsed_seconds"]=round(time.time()-start_clock,2)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {output}; provenance {manifest_path}; duration {n/fps:.6f}s; frames {n}",flush=True)


if __name__=="__main__":
    main()
