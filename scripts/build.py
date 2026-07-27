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


for provider in providers:

    name = provider["name"]
    behavior = provider["behavior"]
    fmt = provider["format"]
    url = provider["url"]

    print(f"\n=== {name} ===")

    source_ext = "yaml" if fmt == "yaml" else "txt"

    source = f"{SOURCE_DIR}/{name}.{source_ext}"
    target = f"{RULESET_DIR}/{name}.mrs"


    print(f"Download: {url}")

    urllib.request.urlretrieve(
        url,
        source
    )


    convert_source = source
    convert_format = fmt


    #
    # Blackmatrix7 YAML
    #
    if behavior == "classical" and fmt == "yaml":

        print("Process classical yaml")

        with open(source, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        payload = data.get("payload", [])

        yaml_source = f"{SOURCE_DIR}/{name}_mihomo.yaml"

        with open(yaml_source, "w", encoding="utf-8") as f:
            yaml.dump(
                {
                    "payload": payload
                },
                f,
                allow_unicode=True,
                sort_keys=False
            )

        convert_source = yaml_source
        convert_format = "yaml"


    #
    # domain text
    #
    elif behavior == "domain" and fmt == "text":

        print("Process domain text")


    #
    # ipcidr text
    #
    elif behavior == "ipcidr" and fmt == "text":

        print("Process ipcidr text")


    print(
        f"Convert {name}.mrs"
    )


    subprocess.run(
        [
            MIHOMO,
            "convert-ruleset",
            behavior,
            convert_format,
            convert_source,
            target
        ],
        check=True
    )


print("\nGenerated rules:")

for file in sorted(os.listdir(RULESET_DIR)):
    if file.endswith(".mrs"):
        print(file)


print("\nDONE")