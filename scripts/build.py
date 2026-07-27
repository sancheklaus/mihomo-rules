import json
import os
import subprocess
import urllib.request
import yaml


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


    # обработка yaml от Blackmatrix7
if fmt == "yaml":

    with open(source, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    payload = data.get("payload", [])

    txt_source = f"{SOURCE_DIR}/{name}.txt"

    with open(txt_source, "w", encoding="utf-8") as f:
        for rule in payload:
            if rule.startswith("DOMAIN,"):
                f.write(rule + "\n")

            elif rule.startswith("DOMAIN-SUFFIX,"):
                f.write(rule + "\n")

            elif rule.startswith("DOMAIN-KEYWORD,"):
                f.write(rule + "\n")

    source = txt_source

    print(f"Build {name}.mrs")


    subprocess.run(
        [
            MIHOMO,
            "convert-ruleset",
            "classical",
            "text",
            source,
            target
        ],
        check=True
    )


print("Generated:")
for f in os.listdir(RULESET_DIR):
    print(f)