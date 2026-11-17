# test_influx.py

import time
import json
from influxdb_client import InfluxDBClient, Point
from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKETS, DEVICE_ID

def write_test_point():
    client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api()
    ts        = int(time.time() * 1000)
    p         = (
        Point("kpis")
        .tag("device_id", DEVICE_ID)
        .field("connectivity_test", 1.0)
        .time(ts, write_precision="ms")
    )
    for bucket in INFLUX_BUCKETS:
        write_api.write(bucket=bucket, org=INFLUX_ORG, record=p)
    print(f"Wrote test point at {ts} to buckets: {INFLUX_BUCKETS}")

def read_test_point(bucket):
    client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    query_api = client.query_api()
    # Query last minute’s connectivity_test for this device
    flux = f'''
        from(bucket: "{bucket}")
          |> range(start: -1m)
          |> filter(fn: (r) =>
               r._measurement == "kpis"
            and r._field == "connectivity_test"
            and r.device_id == "{DEVICE_ID}"
          )
          |> last()
    '''
    tables = query_api.query(flux)
    for table in tables:
        for record in table.records:
            return record.get_value()
    return None

if __name__ == "__main__":
    write_test_point()
    time.sleep(2)  # give InfluxDB a moment to ingest
    for bucket in INFLUX_BUCKETS:
        val = read_test_point(bucket)
        if val is None:
            print(f"❌ No test point found in bucket '{bucket}'")
        else:
            print(f"✔️ Read back from '{bucket}': connectivity_test = {val}")

