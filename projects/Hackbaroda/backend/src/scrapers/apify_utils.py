"""Helpers for Apify client compatibility across SDK versions."""


def get_dataset_id(run) -> str:
    """Get dataset ID from Apify run (dict in v1, Run object in v3+)."""
    if hasattr(run, "default_dataset_id"):
        return run.default_dataset_id
    return run["defaultDatasetId"]
