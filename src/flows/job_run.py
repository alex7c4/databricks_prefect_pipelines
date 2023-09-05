"""Example flow"""
# pylint: disable=duplicate-code
from dataclasses import fields
from datetime import timedelta
from pprint import pprint

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute, jobs
from databricks.sdk.service.compute import Library
from prefect import filesystems, flow, task
from prefect.deployments import Deployment


@task
def make_workspace() -> WorkspaceClient:
    """Authorise Databricks Workspace client"""
    return WorkspaceClient()


@task
def get_existing_job(workspace_client: WorkspaceClient, job_name: str) -> None | jobs.Job:
    """Get most resent existing job fully matched with provided 'job_name'.

    :param workspace_client: Databricks Workspace client
    :param job_name: Name of the job to search
    :return: Job info if job found, otherwise None
    """
    existing_jobs = sorted(
        workspace_client.jobs.list(name=job_name, limit=100), key=lambda x: x.created_time, reverse=True
    )
    if existing_jobs:
        return workspace_client.jobs.get(job_id=existing_jobs[0].job_id)
    return None


@task
def make_job_setting(workspace_client: WorkspaceClient, task_key: str, job_name: str) -> jobs.JobSettings:
    """Create job with tasks description.

    :param workspace_client: Databricks Workspace client
    :param task_key: Task name
    :param job_name: Job name
    :return: JobSettings information
    """
    db_task = jobs.Task(
        notebook_task=jobs.NotebookTask(notebook_path="/master/some/some_notebook", source=jobs.Source.WORKSPACE),
        task_key=task_key,
        run_if=jobs.RunIf.ALL_SUCCESS,
        timeout_seconds=0,
        new_cluster=compute.ClusterSpec(
            spark_version=workspace_client.clusters.select_spark_version(long_term_support=True),
            node_type_id="Standard_DS3_v2",
            driver_node_type_id="Standard_DS3_v2",
            num_workers=0,
            spark_conf={
                "spark.databricks.delta.preview.enabled": True,
                "spark.master": "local[*, 4]",
                "spark.databricks.cluster.profile": "singleNode",
            },
            azure_attributes=compute.AzureAttributes(
                availability=compute.AzureAvailability.ON_DEMAND_AZURE,
                first_on_demand=1,
                spot_bid_max_price=-1,
            ),
            custom_tags={"ResourceClass": "SingleNode"},
            enable_elastic_disk=True,
        ),
        libraries=[Library(whl="dbfs:/FileStore/jars/databricks_pipelines-0.0.1-py3-none-any.whl")],
    )
    db_job = jobs.JobSettings(name=job_name, tasks=[db_task], max_concurrent_runs=1, timeout_seconds=0)
    return db_job


@task
def update_job(workspace_client: WorkspaceClient, job_id: int, job_setting: jobs.JobSettings) -> int:
    """Update existing job with new JobSettings.

    :param workspace_client: Databricks Workspace client
    :param job_id: Existing Job ID
    :param job_setting: New job settings
    :return: Job ID
    """
    print(f"Update existing JobID '{job_id}'")
    workspace_client.jobs.reset(job_id=job_id, new_settings=job_setting)
    return job_id


@task
def create_job(workspace_client: WorkspaceClient, job_setting: jobs.JobSettings) -> int:
    """Create new job.

    :param workspace_client: Databricks Workspace client
    :param job_setting: job settings
    :return: Job ID
    """
    print("Create a new job")
    response = workspace_client.jobs.create(
        **{field.name: getattr(job_setting, field.name) for field in fields(job_setting)}
    )
    job_id: int = response.job_id
    return job_id


@task
def run_job(workspace_client: WorkspaceClient, job_id: str) -> jobs.Run:
    """Run and wait job.

    :param workspace_client: Databricks Workspace client
    :param job_id: Existing Job ID
    :return: Job run information
    """
    return workspace_client.jobs.run_now_and_wait(job_id=job_id, timeout=timedelta(minutes=20))


@flow(name="Run some_notebook", log_prints=True, retries=0)
def main_flow():
    """flow docstring"""
    job_name = "Test job One"
    task_name = "run_some_notebook"

    workspace_client = make_workspace()
    new_job_settings = make_job_setting(workspace_client, task_key=task_name, job_name=job_name)

    existing_job = get_existing_job(workspace_client, job_name=job_name)
    if existing_job:
        # update existing job with job settings
        job_id = update_job(workspace_client, job_id=existing_job.job_id, job_setting=new_job_settings)
    else:
        # create a new job
        job_id = create_job(workspace_client, job_setting=new_job_settings)

    run_info = run_job(workspace_client, job_id=job_id)
    pprint(run_info.as_dict())


def deployment() -> Deployment:
    """deploy docstring"""
    return Deployment.build_from_flow(  # type: ignore
        flow=main_flow,
        name="manual_run",
        tags=["test"],
        storage=filesystems.Azure.load("azure-fs"),
        load_existing=False,
        path="flows2",
        # apply=True,
    )


if __name__ == "__main__":
    # from dotenv import load_dotenv
    # load_dotenv()
    # main_flow()

    deploy = deployment()
    print(f"Deployed '{deploy.flow_name}' as '{deploy.apply()}'")
