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


with open(
    "sources/providers.json",
    encoding="utf-8"
) as f:
    providers = json.load(f)


for provider in providers:

    name = provider["name"]
    behavior = provider["behavior"]
    fmt = provider["format"]
    url = provider["url"]


    print("")
    print("======================")
    print(name)
    print("======================")


    source_ext = "yaml" if fmt == "yaml" else "txt"

    source = f"{SOURCE_DIR}/{name}.{source_ext}"
    target = f"{RULESET_DIR}/{name}.mrs"


    print("Download:")
    print(url)


    urllib.request.urlretrieve(
        url,
        source
    )


    convert_behavior = behavior
    convert_format = fmt
    convert_source = source


    #
    # Blackmatrix7 Clash YAML
    #
    if behavior == "classical" and fmt == "yaml":

        print("Convert classical yaml -> domain text")


        with open(
            source,
            encoding="utf-8"
        ) as f:
            data = yaml.safe_load(f)


        payload = data.get(
            "payload",
            []
        )


        txt_source = (
            f"{SOURCE_DIR}/{name}_domain.txt"
        )


        with open(
            txt_source,
            "w",
            encoding="utf-8"
        ) as f:

            for rule in payload:

                if not isinstance(rule, str):
                    continue


                if rule.startswith(
                    "DOMAIN-SUFFIX,"
                ):

                    domain = rule.split(
                        ",",
                        1
                    )[1]

                    f.write(
                        domain + "\n"
                    )


                elif rule.startswith(
                    "DOMAIN,"
                ):

                    domain = rule.split(
                        ",",
                        1
                    )[1]

                    f.write(
                        domain + "\n"
                    )


        convert_behavior = "domain"
        convert_format = "text"
        convert_source = txt_source


    #
    # Direct domain list
    #
    elif behavior == "domain":

        print(
            "Convert domain text"
        )


    #
    # Direct IP list
    #
    elif behavior == "ipcidr":

        print(
            "Convert ipcidr text"
        )


    print(
        f"Build {name}.mrs"
    )


    subprocess.run(
        [
            MIHOMO,
            "convert-ruleset",
            convert_behavior,
            convert_format,
            convert_source,
            target
        ],
        check=True
    )


print("")
print("Generated rules:")


for file in sorted(
    os.listdir(RULESET_DIR)
):

    if file.endswith(".mrs"):

        print(file)


print("")
print("DONE")