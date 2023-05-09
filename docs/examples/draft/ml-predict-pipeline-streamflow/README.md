# DeepHealth Pipelines


## Configure

To modify the location where data are stored, create ```.env``` file executing:
```
./create_env.sh
```
Then edit properly the output ```.env```. Be sure to set safe user/password values.


Edit env variable ```CWL_DOCKER_GPUS ``` for setting the gpus to be used on docker container used for predictions.

N.B
Change ```omeseadragon:4080``` in ome_seadragon.base_url and ome_seadragon.static_files_url to the local machine address.
The port is the same specified in omeseadragon-nginx service (docker-compose.omero.yaml).

## Deploy

```
./compose.sh up -d
```

Check if ```init``` service exited with 0 code, otherwise restart it. It can fail for timing reason, typically sql tables do not exist yet.

To visit Airflow, go to http://localhost:<AIRFLOW_WEBSERVER_PORT>.



## Upload data

```
cd slide-importer
docker build -t slide-importer .
```

To import a slide, run:
```
. .env #docker-compose env file for airflow
docker run --rm -it -v $CWL_INPUTS_FOLDER:$CWL_INPUTS_FOLDER -v /PATH/TO/SLIDE:/upload --network deephealth-pipelines_default     slide-importer --server-url http://webserver:8080 /upload/SLIDE_FILENAME --user admin
```

It wil prompt asking the airflow password.




