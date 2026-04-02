import requests
import json

url = "http://localhost:4318/v1/logs"

data = {
    "resourceLogs": [{
        "resource": {
            "attributes": [
                {"key": "service.name", "value": {"stringValue": "manual-test"}}
            ]
        },
        "scopeLogs": [{
            "logRecords": [{
                "body": {"stringValue": "DBS-Level-Log-Check-Successful"},
                "severityText": "INFO"
            }]
        }]
    }]
}
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
