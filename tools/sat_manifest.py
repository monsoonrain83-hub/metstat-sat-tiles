"""Assemble manifest.json for the published site from per-layer meta.json files. Marks a layer stale if observation older than 90 min."""
import json, glob, os, datetime as dt, sys
root=sys.argv[1]; now=dt.datetime.utcnow(); M={"generated_utc":now.isoformat()+"Z","source":"EUMETSAT EUMETView WMS (public). Tiles: EPSG:3857 XYZ 512px, WebP.","layers":{}}
for p in glob.glob(root+"/*/meta.json"):
    m=json.load(open(p)); name=os.path.basename(os.path.dirname(p))
    obs=dt.datetime.strptime(m["observation_time_utc"][:19],"%Y-%m-%dT%H:%M:%S")
    m["age_min"]=round((now-obs).total_seconds()/60); m["stale"]=m["age_min"]>90; m["tiles_path"]=name+"/{z}/{x}/{y}.webp"; M["layers"][name]=m
json.dump(M,open(root+"/manifest.json","w"),indent=1); print(json.dumps({k:(v["observation_time_utc"],v["tiles_ok"],v["tiles_failed"]) for k,v in M["layers"].items()}))
