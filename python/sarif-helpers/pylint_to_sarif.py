import json
import sys
import uuid
from datetime import datetime

def map_severity(pylint_type):
    # Map Pylint types to SARIF severity levels
    severity_map = {
        "convention": "note",
        "refactor": "note",
        "warning": "warning",
        "error": "error",
        "fatal": "error"
    }
    return severity_map.get(pylint_type, "note")

def convert_pylint_to_sarif(pylint_json):
    sarif = {
        "version": "2.1.0",
        "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Pylint",
                        "version": "3.3.3",
                        "informationUri": "https://pylint.pycqa.org/",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }

    rules = {}
    results = []

    for issue in pylint_json:
        rule_id = issue["message-id"]
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "shortDescription": {
                    "text": issue["symbol"]
                },
                "fullDescription": {
                    "text": issue["message"]
                },
                "defaultConfiguration": {
                    "level": map_severity(issue["type"])  # Map severity based on type
                }
            }
        ## Fixing the column issue with minimum value of 1
        if issue["column"] == 0:
            issue["column"] = 1
        result = {
            "ruleId": rule_id,
            "message": {
                "text": issue["message"]
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": issue["path"]
                        },
                        "region": {
                            "startLine": issue["line"],
                            "startColumn": issue["column"]
                        }
                    }
                }
            ]
        }

        results.append(result)

    sarif["runs"][0]["tool"]["driver"]["rules"] = list(rules.values())
    sarif["runs"][0]["results"] = results

    return sarif

def main():
    if len(sys.argv) != 3:
        print("Usage: python pylint_to_sarif.py <pylint_json_file> <sarif_output_file>")
        sys.exit(1)

    pylint_json_file = sys.argv[1]
    sarif_output_file = sys.argv[2]

    with open(pylint_json_file, 'r') as f:
        pylint_json = json.load(f)

    sarif = convert_pylint_to_sarif(pylint_json)

    with open(sarif_output_file, 'w') as f:
        json.dump(sarif, f, indent=2)

    print(f"SARIF output written to {sarif_output_file}")

if __name__ == "__main__":
    main()