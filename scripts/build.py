import json
import os
import subprocess
import urllib.request


MIHOMO = "./mihomo"
SOURCE_DIR = "sources"
RULESET_DIR = "ruleset"


os.makedirs(SOURCE_DIR, exist_ok=True)
os.makedirs(RULESET_DIR, exist_ok=True)


with open("sources/providers.json", encoding="utf-8") as f:
    providers = json.load(f)


for p in providers:

    name = p["name"]
    behavior = p["behavior"]
    fmt = p["format"]

    ext = "yaml" if fmt == "yaml" else "txt"

    source = f"{SOURCE_DIR}/{name}.{ext}"
    target = f"{RULESET_DIR}/{name}.mrs"


    print(f"Download {name}")

    urllib.request.urlretrieve(
        p["url"],
        source
    )


    print(f"Build {name}.mrs")


    subprocess.run(
        [
            MIHOMO,
            "convert-ruleset",
            behavior,
            fmt,
            source,
            target
        ],
        check=True
    )


print("DONE")