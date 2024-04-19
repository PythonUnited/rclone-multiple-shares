# Periodic Rclone syncer

The official rclone docker image suffices when periodically pulling files of cloud storage. 
For example when using this config: 

    services:
      rclone:
        image: rclone/rclone:latest
        restart: always
        volumes:
          - ./config/rclone/rclone.conf:/config/rclone.conf
          - ./dropbox:/opt/sync
        entrypoint:
          sh -c "
            rclone sync
              --config /config/rclone.conf --progress --delete-after --create-empty-src-dirs --include *.xlsx 
              ${RCLONE_PATH} /opt/sync
            && echo \"sleeping for ${RCLONE_SLEEP_SECONDS} seconds\"  && sleep ${RCLONE_SLEEP_SECONDS}
          "

However, the official does not support syncing multiple paths from cloud storage, nor is cron scheduling support. 
This docker image aims to solve these missing features.

## Caveat 

This Docker image was created for pulling files of a Dropbox share. With adjustments it could work for multiple storage 
providers, currently only one storage provider (in `./config/rclone.conf`) is supported. Pushing files could be possible 
with some changes.

## Getting started

Copy example config files:

```bash
cp env-template .env
cp ./config/rclone.conf-template ./config/rclone.conf
cp ./config/rclone-mapping.json-template ./config/rclone-mapping.json
```

Edit `.env` and set your user and group ID. This is needed so the file permissions match with the one in the rclone 
container. This file is also used to configure the cron frequency using `CRON_SCHEDULE`.

See [rclone docs](https://rclone.org/docs/) for the contents of `rclone.conf`.

The `rclone-mapping.json` is used to configure the folders.

```json
{
  "files": [
    {
      "id": "example",
      "path": "remote_folder",
      "include": "*.xlsx"
    }
  ]
}
```

With the json example all `*.xlsx` files in the folder `remote_folder` in cloud storage are pulled to a local folder 
`example`. The docker compose container is configured to sync the files to the `./sync/` folder. With this example 
files are copied to `./sync/example/`.

First build the image using `docker compose build`. Or use the image hosted at docker hub, replace the `build` section in `docker-compose.yml` with `image: pythonunitednl/rclone-multiple-shares`. Finally start the container using `docker compose up`. On each run in cron output is logged to `/tmp/cron.log`.
