    dg list defs

    dg list components

First, create a new component for running Databricks jobs:

    dg scaffold component ACMEDatabricksJobComponent

Then, update the component adapting it from our ML engineer's script:

**COPY AND PASTE**

```python
import os

import dagster as dg

from databricks.sdk import WorkspaceClient

class ACMEDatabricksJobComponent(dg.Component, dg.Model, dg.Resolvable):
    """Component for running a Databricks job by ID, and attaching assets"""

    # added fields here will define params when instantiated in Python, and yaml schema via Resolvable
    job_id: int
    parameters: dict[str, str]
    databricks_host: str
    databricks_token: str
    assets: list[dg.ResolvedAssetSpec]


    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.multi_asset(name=f"{self.job_id}_assets", specs=self.assets)
        def _multi_asset(context: dg.AssetExecutionContext) -> dg.AssetExecutionContext:
            client = WorkspaceClient(host=self.databricks_host, token=self.databricks_token)
            client.jobs.run_now_and_wait(
                job_id=self.job_id,
                job_parameters=self.parameters,
            )

        return dg.Definitions(assets=[_multi_asset])
```

    dg list components

Next, scaffold the definition instance for that component:

    dg scaffold defs dagster_demo.components.acme_databricks_job_component.ACMEDatabricksJobComponent colton_dbx_report

Next, populate the YAML for your new component:

```yaml
type: dagster_demo.components.acme_databricks_job_component.ACMEDatabricksJobComponent

attributes:
  job_id: 1000180891217799
  parameters:
    source_file_prefix: "s3://acme-analytics/raw"
    destination_file_prefix: "s3://acme-analytics/reports"
  databricks_host: "{{ env.DATABRICKS_HOST }}"
  databricks_token: "{{ env.DATABRICKS_TOKEN }}"
  assets:
    - key: colton_dbx_annual_report
      owners:
        - colton@dagsterlabs.com
      kinds:
        - databricks
        - csv
```

Validate

    dg check defs

    dg list defs

Make it downstream of our existing assets...

      deps:
        - prepared_accounts

And finally, add another definition, copy and paste the YAML inline `---`

NOTE: demonstrate a typo, and then perform:

    dg check yaml

```yaml
type: dagster_demo.components.acme_databricks_job_component.ACMEDatabricksJobComponent

attributes:
  job_id: 1000180891217799
  parameters:
    source_file_prefix: "s3://acme-analytics/raw"
    destination_file_prefix: "s3://acme-analytics/reports"
  databricks_host: "{{ env.DATABRICKS_HOST }}"
  databricks_token: "{{ env.DATABRICKS_TOKEN }}"
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

type: dagster_demo.components.acme_databricks_job_component.ACMEDatabricksJobComponent

attributes:
  job_id: 123
  parameters:
    source_file_prefix: "s3://acme-analytics/raw"
    destination_file_prefix: "s3://acme-analytics/reports"
  databricks_host: "{{ env.DATABRICKS_HOST }}"
  databricks_token: "{{ env.DATABRICKS_TOKEN }}"
  assets:
    - key: nick_dbx_annual_report
      owners:
        - nick@dagsterlabs.com
      kinds:
        - databricks
        - csv
      deps:
        - prepared_accounts
```
