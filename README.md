# phuzzerUI
WebUI for dronefuzz project 

## Build
```
./build
```
## Run
```
Usage: ./run [OPTIONS] <port> (Defaults to port 8888)

OPTIONS:
-h    Print this Help.
-d    Debug mode, runs container with interactive shell instead of WebUI.
```


## CI Monitoring
Include the WebUI code inside the docker container used for fuzzing which is run by the CI, and run the WebUI start.sh
Another option is to keep the WebUI docker container seprate and just mount the fuzz-master log path to the WebUI.


UI will default to monitroing `/dev/shm/work/` and looks for `fuzzer-master.log` as indicator of CI starting the fuzzer, it will also pull info from the same path.
once the log is removed the UI will stop monitoring.


To change the log path to monitor simply modify last line in `src/app.py`
