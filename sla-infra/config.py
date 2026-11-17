# config.py

# InfluxDB connection details
INFLUX_URL    = "http://100.99.1.11:8086"
INFLUX_TOKEN  = "Gj4IQyumYQ4jq7iaydS7DJTfrN6gyMwyCbAYy3GqzvyFVNOr8Cx-oU6n7oGbYb_R2FgmxT3eoFKAQ8fUpAhu4A=="
INFLUX_ORG    = "my-org"

# List all the buckets where your KPIs live
INFLUX_BUCKETS = [
   "wifi1_bucket",
   "4g_cellular_bucket",
   "5g_cellular_bucket",
   "blackbox_hwmon_bucket",
   "blackbox_kpi_bucket",
   "blackbox_network_bucket",
   "blackbox_vibration_bucket",
   "blackbox_kpi_bucket",
   "wifi_ap_bucket",
    # add more buckets as needed
]

# Unique identifier for this device
DEVICE_ID = "device-1234"

# Path to your SLA policy file (JSON or YAML)
SLA_POLICY_FILE = "sla_policies.json"

# How often (in seconds) to poll InfluxDB and re-evaluate SLAs
POLL_INTERVAL_SECONDS = 60

