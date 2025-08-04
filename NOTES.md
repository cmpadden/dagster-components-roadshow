First, create a new component for running Databricks jobs:

    dg scaffold component DatabricksJobComponent

Then, update the component adapting it from our ML engineer's script:

    import os

    import dagster as dg

    DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")

    class DatabricksJobComponent(dg.Component, dg.Model, dg.Resolvable):
        """Component for running Databricks jobs, and attaching assets"""

        # added fields here will define params when instantiated in Python, and yaml schema via Resolvable
        job_id: int
        parameters: dict[str, str]
        assets: list[dg.ResolvedAssetSpec]

        def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
            @dg.multi_asset(name=f"{self.job_id}_assets", specs=self.assets)
            def _multi_asset(context: dg.AssetExecutionContext) -> dg.AssetExecutionContext:
                client = WorkspaceClient(host=self.host, token=self.token)
                client.jobs.run_now_and_wait(
                    job_id=self.job_id,
                    job_parameters=self.parameters,
                )

            return dg.Definitions(assets=[_multi_asset])

Next, scaffold the definition instance for that component:

    dg scaffold defs dagster_demo_runpod.components.databricks_job_component.DatabricksJobComponent colton_dbx_job


Next, populate the YAML for your new component:

    type: dagster_demo_runpod.components.databricks_job_component.DatabricksJobComponent

    attributes:
      job_id: 1000180891217799
      parameters:
        source_file_prefix: "s3://acme-analytics/raw"
        destination_file_prefix: "s3://acme-analytics/reports"
      assets:
        - key: colton_dbx_annual_report
          owners:
            - colton@dagsterlabs.com
          kinds:
            - databricks
            - csv

Validate

    dg check defs

    dg list defs

Make it downstream of our existing assets...

      deps:
        - prepared_accounts

And finally, add another definition, copy and paste the YAML inline `---`

    type: dagster_demo_runpod.components.databricks_job_component.DatabricksJobComponent

    attributes:
      job_id: 1000180891217799
      parameters:
        source_file_prefix: "s3://acme-analytics/raw"
        destination_file_prefix: "s3://acme-analytics/reports"
      assets:
        - key: colton_dbx_annual_report
          owners:
            - colton@dagsterlabs.com
          kinds:
            - databricks
            - csv
          deps:
            - prepared_accounts

    ---

    type: dagster_demo_runpod.components.databricks_job_component.DatabricksJobComponent

    attributes:
      job_id: 123
      parameters:
        source_file_prefix: "s3://acme-analytics/raw"
        destination_file_prefix: "s3://acme-analytics/reports"
      assets:
        - key: nick_dbx_annual_report
          owners:
            - nick@dagsterlabs.com
          kinds:
            - databricks
            - csv
          deps:
            - prepared_accounts

