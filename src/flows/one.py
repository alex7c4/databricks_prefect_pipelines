"""Example flow"""
# pylint: disable=duplicate-code
from prefect import filesystems, flow, task
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule


@task
def some_task(user_name: str) -> str:
    """some task"""
    return f"Hello from task from {user_name}"


@flow(name="One", log_prints=True)
def main_flow(user: str = "User"):
    """flow docstring"""
    print(some_task(user_name=user))


def deployment() -> Deployment:
    """deploy docstring"""
    return Deployment.build_from_flow(  # type: ignore
        flow=main_flow,
        name="daily_run",
        schedule=CronSchedule(cron="0 9 * * *", timezone="America/Chicago"),
        tags=["test"],
        storage=filesystems.Azure.load("azure-fs"),
        load_existing=False,
        # skip_upload=True,
        # apply=True,
        path="flows",
    )


if __name__ == "__main__":
    # main_flow()
    deploy = deployment()
    print(f"Deployed '{deploy.flow_name}' as '{deploy.apply()}'")
