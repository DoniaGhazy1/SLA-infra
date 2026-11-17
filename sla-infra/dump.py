# runner.py

import time
import csv
import os
from datetime import datetime
from influxdb_client import InfluxDBClient
from config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKETS,
    POLL_INTERVAL_SECONDS,
    DEVICE_ID,
)
from storage.influx_query import fetch_kpi_aggregate

# CSV setup
LOG_FILE = "kpi_dump.csv"
CSV_HEADER = ["timestamp", "device_id", "bucket", "measurement", "field", "value"]

def log_reading(device_id, bucket, measurement, field, value):
    """Append one row to kpi_dump.csv."""
    is_new = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(CSV_HEADER)
        writer.writerow([
            datetime.utcnow().isoformat(),
            device_id,
            bucket,
            measurement,
            field,
            value
        ])

def discover_measurements(client, bucket):
    """Return a list of measurement names in the given bucket."""
    query_api = client.query_api()
    flux = f'''
import "influxdata/influxdb/schema"
schema.measurements(bucket: "{bucket}")
'''
    tables = query_api.query(flux)
    return [
        record.get_value()
        for table in tables
        for record in table.records
    ]

def discover_fields(client, bucket, measurement):
    """Return a list of field keys in the given bucket+measurement."""
    query_api = client.query_api()
    flux = f'''
import "influxdata/influxdb/schema"
schema.fieldKeys(bucket: "{bucket}")
  |> filter(fn: (r) => r._measurement == "{measurement}")
'''
    tables = query_api.query(flux)
    return [
        record.get_value()
        for table in tables
        for record in table.records
    ]

def main_loop():
    # Initialize InfluxDB client once
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    while True:
        loop_start = time.time()

        for bucket in INFLUX_BUCKETS:
            # 1. Discover measurements in this bucket
            measurements = discover_measurements(client, bucket)
            for meas in measurements:
                # 2. Discover fields in each measurement
                fields = discover_fields(client, bucket, meas)
                for field in fields:
                    # 3. Fetch the mean over the last poll interval
                    window = f"{POLL_INTERVAL_SECONDS}s"
                    value = fetch_kpi_aggregate(
                        bucket=bucket,
                        measurement=meas,
                        field=field,
                        device_id=DEVICE_ID,
                        window=window
                    )
                    # 4. Log it
                    log_reading(DEVICE_ID, bucket, meas, field, value)

        # Sleep until next round
        elapsed = time.time() - loop_start
        time.sleep(max(0, POLL_INTERVAL_SECONDS - elapsed))

if __name__ == "__main__":
    main_loop()

