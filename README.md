Training project to make Prefect managed Databricks pipelines.
CI should run checks and tests and, if successful, deploy the notebooks to the Databriks server.

---
WIP:

```shell
docker compose up --remove-orphans --force-recreate --pull always

docker compose down --volumes
docker compose down --rmi all --volumes
docker system prune --all --volumes --force
```

Minio: http://localhost:9090

```shell
docker run -it \
    -v /Users/Aleksandr_Koriagin/work/personal/databr_pipelines:/root/databr_pipelines \
    --workdir /root/databr_pipelines \
    prefecthq/prefect:2-python3.11 bash ;


export PYTHONPATH=$(pwd)

python ./src/flows/one.py && python ./src/flows/two.py && python ./src/flows/three.py
prefect agent start --pool default-agent-pool --work-queue default


docker exec -it databr_pipelines-cli-1 bash
prefect cloud login -k xxxxxx
python one.py
```

`src/scripts/upload_notebooks.py`
