"""Example flow"""
from prefect import flow
from prefect.deployments import Deployment


@flow(name="Two", log_prints=True)
def main_flow():
    """flow docstring"""
    print("Hi from Prefect: Flow Two")


def deploy():
    """deploy docstring"""

    deployment = Deployment.build_from_flow(
        flow=main_flow,
        name="daily_run",
        # schedule=CronSchedule(cron="0 9 * * *", timezone="America/Chicago"),
        tags=["test"],
        apply=True,
        # storage=minio_block,
    )
    print(deployment)


if __name__ == "__main__":
    deploy()
