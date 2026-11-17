# storage/logging.py

import csv
import os
from datetime import datetime

LOG_FILE = "sla_readings.csv"
HEADER = ["timestamp", "device_id", "bucket", "measurement", "field", "value"]

def log_reading(device_id, bucket, measurement, field, value):
    """
    Append one row to sla_readings.csv with the current UTC time
    and the fetched KPI value.
    """
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerow([
            datetime.utcnow().isoformat(),
            device_id,
            bucket,
            measurement,
            field,
            value
        ])

