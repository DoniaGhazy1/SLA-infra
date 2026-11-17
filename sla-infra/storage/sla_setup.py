# storage/influx_setup.py

from influxdb_client import InfluxDBClient, BucketRetentionRules
from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG

def ensure_bucket(name: str, retention_hours: int = 24*30) -> bool:
    """
    Create the bucket `name` if it doesn’t already exist.
    Returns True if created, False if it already existed.
    """
    client      = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    buckets_api = client.buckets_api()

    existing = [b.name for b in buckets_api.find_buckets().buckets]
    if name in existing:
        return False

    retention = BucketRetentionRules(type="expire", every_seconds=retention_hours * 3600)
    buckets_api.create_bucket(bucket_name=name, org=INFLUX_ORG, retention_rules=[retention])
    return True

