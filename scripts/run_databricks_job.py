import os

from databricks.sdk import WorkspaceClient

# Access Databricks environment connection details from environment variables
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")

if __name__ == "__main__":
    # The ID of the job we are running in Databricks that produces CSV reporting files
    databricks_job_id = 1000180891217799

    # The parameters being passed to our notebook job
    job_parameters = {
        "source_file_prefix": "s3://acme-analytics/raw",
        "destination_file_prefix": "s3://acme-analytics/reports",
    }

    # Run our job and wait for completion using the `databricks-sdk`
    client = WorkspaceClient(host=DATABRICKS_HOST, token=DATABRICKS_TOKEN)
    client.jobs.run_now_and_wait(
        job_id=databricks_job_id,
        job_parameters=job_parameters,
    )