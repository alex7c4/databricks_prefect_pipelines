from prefect import filesystems, flow, task
from prefect.deployments import Deployment

from src.flows.dummy import main_flow as dummy_flow
from src.flows.job_run import main_flow as databricks_job_run_flow
from src.flows_lib.dummy import dummy_func


@task
def task_1(val: int) -> str:
    """some task"""
    return f"Run this task with '{val}'"


@flow(name="Wait another flows", log_prints=True)
def main_flow():
    """flow docstring"""
    _ = databricks_job_run_flow()  # wait another flow
    _ = dummy_flow()  # wait another flow
    print(task_1(val=dummy_func()))


def deployment() -> Deployment:
    """deploy docstring"""
    return Deployment.build_from_flow(  # type: ignore
        flow=main_flow,
        name="daily_run",
        tags=["test"],
        storage=filesystems.Azure.load("azure-fs"),
        load_existing=False,
        path="flows2",
    )


if __name__ == "__main__":
    deploy = deployment()
    print(f"Deployed '{deploy.flow_name}' as '{deploy.apply()}'")
