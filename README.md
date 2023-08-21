**Training project to make Prefect managed Databricks pipelines.**

CI _(Github Actions)_ will run checks and unit tests and, if successful, deploy the notebooks and python lib to the Databriks server.

> [!NOTE]  
> This project is still in WIP

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
