import dagster as dg

ASSET_OWNERS = ["bob@runpod.io"]


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_transactions], owners=ASSET_OWNERS)
def prepared_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "parquet",
            "transformations_applied": [
                "category_classification",
                "large_transaction_flag",
            ],
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_customers], owners=ASSET_OWNERS)
def prepared_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "parquet",
            "transformations_applied": ["days_since_signup", "premium_flag"],
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_accounts], owners=ASSET_OWNERS)
def prepared_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    return dg.MaterializeResult(
        metadata={
            "file_format": "parquet",
            "transformations_applied": ["balance_tier", "days_active"],
        }
    )
