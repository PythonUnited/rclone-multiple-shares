#!/usr/bin/python
import configparser
import json
import os
import subprocess

print("=" * 80)

config = configparser.ConfigParser()
config.read("/config/rclone.conf")
dropbox_share = config.sections()[0]

with open("/config/mapping.json", "r") as fh:
    mapping = json.loads(fh.read())
    dropbox_files = mapping["files"]


for dropbox_file in dropbox_files:
    file_id = dropbox_file["id"]
    local_dir = os.path.join("/opt/sync/", file_id)
    dropbox_path = dropbox_file["path"]
    file_include = dropbox_file["include"]

    print("Syncing {} {}".format(file_id, dropbox_path))

    command = [
        "rclone",
        "--config",
        "/config/rclone.conf",
        "--delete-after",
        f"--include",
        file_include,
        "sync",
        f"{dropbox_share}:{dropbox_path}",
        local_dir,
    ]
    print(" ".join(command))
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("** Sync failed **")
        print("Command failed with return code:", result.returncode)
        print("Error output:")
        print(result.stderr)

    print("-" * 80)
