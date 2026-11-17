# storage/sla_writer.py

from influxdb_client import InfluxDBClient, Point
from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG

# Initialize once at import
_client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
_write_api = _client.write_api()

def write_sla_status(rule, value: float, passed: bool, timestamp_ms: int):
    """
    Writes one point per SLA rule to the `sla_status` bucket and prints confirmation.
    - rule: your SlaRule object (has device_id, bucket, measurement, field, id, severity)
    - value: the numeric KPI you just fetched
    - passed: True if SLA passed, False if it failed
    - timestamp_ms: epoch time in milliseconds
    """
    p = (
        Point("sla_status")
          .tag("device_id",     rule.device_id)
          .tag("source_bucket", rule.bucket)
          .tag("measurement",   rule.measurement)
          .tag("field",         rule.field)
          .tag("rule_id",       str(rule.id))
          .tag("severity",      rule.severity)
          .field("passed",      int(passed))
          .field("value",       float(value))
          .time(timestamp_ms, write_precision="ms")
    )
    # Write to InfluxDB
    _write_api.write(bucket="sla_status", org=INFLUX_ORG, record=p)

    # Print confirmation message
    status_str = "PASS" if passed else "FAIL"
    print(f"[SLA_STATUS] {status_str} device={rule.device_id} "
          f"{rule.bucket}/{rule.measurement} {rule.field}={value} "
          f"at {timestamp_ms}")