python server to replace `api.commadotai.com`. 

update `tools/lib/api.py` and replace `https://api.commadotai.com` with `http://XX.XX.XX.XX:8080`

sample compose.yml to ruyn pyServer with `docker compose`

replace `XX.XX.XX.XX` with the IP of the NFS Server
replace `NFS_PATH` witgh the NFS path to the recordings

```
services:
  python:
    build: .
    image: pyserver
    volumes:
      - rec_data:/recordings/
    ports:
      - 8080:8080
    restart: unless-stopped


volumes:
  rec_data:
    driver_opts:
      type: nfs
      o: addr=XX.XX.XX.XX,rw,hard,vers=4
      device: : NFS_PATH
```

Folder structure for the `recordings` folder.

```
2023-12-26--16-19-38
  2023-12-26--16-19-38--0
  2023-12-26--16-19-38--1
  2023-12-26--16-19-38--2
  2023-12-26--16-19-38--3
2023-12-27--16-19-38
  2023-12-27--16-19-38--0
  2023-12-27--16-19-38--1
  2023-12-27--16-19-38--2
  2023-12-27--16-19-38--3
2023-12-28--16-19-38
  2023-12-28--16-19-38--0
  2023-12-28--16-19-38--1
  2023-12-28--16-19-38--2
  2023-12-28--16-19-38--3
2023-12-29--16-19-38
  2023-12-29--16-19-38--0
  2023-12-29--16-19-38--1
  2023-12-29--16-19-38--2
  2023-12-29--16-19-38--3
2023-12-30--16-19-38
  2023-12-30--16-19-38--0
  2023-12-30--16-19-38--1
  2023-12-30--16-19-38--2
  2023-12-30--16-19-38--3
```
# `sincop` tool
Tool to copy the missing routed from your comma device to your `recordings` folder. Update syncop and replace `RECORDINGS_FOLDER` with the path where `recordigns` should be stored.

# Important Notes:
- The tool was tested using a local path, mount the NFS volume to a local folder and use that path for `RECORDINGS_FOLDER`

- the envirnemnt needs to be configured for the following command to SSH directly to c3x, no user intervention `ssh comma@comma`
