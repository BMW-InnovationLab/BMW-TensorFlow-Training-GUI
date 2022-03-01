import json
import os

base_path = './'

proxy_file_path = os.path.join(base_path, "proxy.json")

proxy_settings = None

with open(proxy_file_path, "r") as proxy_file:
    proxy_settings = json.loads(proxy_file.read())
    

compose_build_files = ["./build_gpu.yml","./build_cpu.yml"]
for build_file in compose_build_files:
    content = None
    with open(build_file, "r") as f:
        lines= f.readlines()

    for i in range(len(lines)):
        if "proxy" in lines[i]:
            parts = lines[i].split(":")
            parts[1] = "\n"
            for setting in proxy_settings.keys():
                if parts[0].endswith(setting.lower()):
                    lines[i] = ""
                    lines[i] = parts[0]+": "+proxy_settings[setting]+parts[1]


    content_to_write = ""
    for line in lines:
        content_to_write += line

    
    with open(build_file, "w") as f:
        f.write(content_to_write)




