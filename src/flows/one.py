"""Example flow"""
from prefect import flow
from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.server.schemas.schedules import CronSchedule


@flow(name="One", log_prints=True)
def main_flow():
    """flow docstring"""
    print("Hi from Prefect: Flow One")


def deploy():
    """deploy docstring"""

    minio_block = RemoteFileSystem(
        basepath="s3://flows",
        settings={
            "key": "aJFHyZQTwOHi1MVAP3gv",
            "secret": "KW7Asnh50iRUxLwMDVno6o8ACH5BT6i6luqrpZgT",
            "client_kwargs": {"endpoint_url": "http://minio:9000"},
        },
    )

    deployment = Deployment.build_from_flow(
        flow=main_flow,
        name="daily_run",
        schedule=CronSchedule(cron="0 9 * * *", timezone="America/Chicago"),
        tags=["test"],
        apply=True,
        storage=minio_block,
    )
    print(deployment)


if __name__ == "__main__":
    deploy()
