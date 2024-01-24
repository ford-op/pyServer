Saample compose.yml

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