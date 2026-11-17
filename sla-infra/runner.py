# runner.py

import time
import json
from storage.influx_query import fetch_kpi_aggregate
from rules.evaluator import eval_condition
from config import DEVICE_ID, SLA_POLICY_FILE, POLL_INTERVAL_SECONDS
from rules.model import SlaRule
from storage.logging     import log_reading
from storage.sla_writer import write_sla_status
from storage.sla_setup import ensure_bucket

"""
def load_sla_rules():
    with open(SLA_POLICY_FILE) as f:
        all_rules = json.load(f)
    # Keep only rules for this device
    return [SlaRule(**r) for r in all_rules if r["device_id"] == DEVICE_ID]
"""
sla_created= ensure_bucket("sla_status", retention_hours=24*30)
if sla_created:
    print("Created new bucket 'sla_status'")
else:
    print("Bucket 'sla_status' already exists")

def load_sla_rules():
    """
    Load SLA rules from JSON, filter by DEVICE_ID, and assign rule IDs.
    """
    sla_rules = []
    with open(SLA_POLICY_FILE) as f:
        all_rules = json.load(f)
    for idx, r in enumerate(all_rules):
        if r.get("device_id") == DEVICE_ID:
            # Insert the rule's array index as its id
            r["id"] = idx
            sla_rules.append(SlaRule(**r))
    return sla_rules

def handle_violation(rule: SlaRule, value: float):
    print(f"[VIOLATION] {rule.bucket}/{rule.measurement}"
          f" {rule.field}={value} !{rule.condition}"
          f" (severity={rule.severity})")

def main_loop():
    sla_rules = load_sla_rules()

    while True:
        start = time.time()

        for rule in sla_rules:
            val = fetch_kpi_aggregate(
                bucket=rule.bucket,
                measurement=rule.measurement,
                field=rule.field,
                device_id=DEVICE_ID,
                window=rule.window
            )
            
            log_reading(DEVICE_ID, rule.bucket, rule.measurement, rule.field, val) #write them inside the CSV file
            print("Data saved in CVS")            

            passed = eval_condition(val, rule.condition)

            if passed:
                print(f"[PASS] device={rule.device_id} {rule.field}={val} meets {rule.condition}")
            else:
                print(f"[FAIL] device={rule.device_id} {rule.field}={val} violates {rule.condition}")
                handle_violation(rule, val)
        
            timestamp_ms= int(time.time()*1000)
            write_sla_status(rule, val, passed, timestamp_ms)

        # calculate scheduling time (configurable)
        elapsed = time.time() - start
        time.sleep(max(0, POLL_INTERVAL_SECONDS - elapsed))

if __name__ == "__main__":
    main_loop()

