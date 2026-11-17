# storage/influx_query.py

from influxdb_client import InfluxDBClient
from config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG

_client    = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
_query_api = _client.query_api()

def fetch_kpi_aggregate(bucket: str,
                        measurement: str,
                        field: str,
                        device_id: str,
                        window: str) -> float:
    """
    Query InfluxDB for the mean value of `field` in `measurement`
    for a specific device over the past `window` (e.g. "1h").
    Returns the last aggregated value or 0.0 if none found.
    """
    flux = f'''
from(bucket: "{bucket}")
  |> range(start: -{window})
  |> filter(fn: (r) =>
       r._measurement == "{measurement}"
    and r._field == "{field}"
  )
  |> aggregateWindow(every: {window}, fn: mean, createEmpty: false)
  |> last()
'''
    tables = _query_api.query(flux)
    for table in tables:
        for record in table.records:
            return float(record.get_value())
    return 0.0

