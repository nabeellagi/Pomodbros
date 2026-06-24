# Automate changing version number and other details to minimize human error because i am lowkey tweaking
# Change version.txt for updates

import json
from pathlib import Path

config = {}

with open("version.txt", "r") as f:
    for line in f:
        line = line.strip()
        
        if not line or "=" not in line:
            continue
        
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()
        
name = config.get("name")
version = config.get("version")
description = config.get("description")

keywords = [
    k.strip() for k in config.get("keywords", "").split(",") if k.strip()
]

json_files = [
    "app/package.json",
    "electron/package.json",
]

for file_path in json_files:
    path = Path(file_path)
    
    if not path.exists():
        print(f"File {file_path} does not exist. Skipping.")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Data attributes goes here
    if name:
        data["name"] = name
    if version:
        data["version"] = version
    if description:
        data["description"] = description
    if keywords:
        data["keywords"] = keywords
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"Updated {file_path} successfully.")