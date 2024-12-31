import json
import sys
import uuid
from datetime import datetime

def convert_pylint_to_sarif(pylint_json):
    sarif = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Pylint",
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
                    "level": issue["type"]
                }
            }

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
    print("Converting Pylint JSON to SARIF format...")
    if len(sys.argv) != 3:
        print("Usage: python pylint_to_sarif.py <pylint_json_file> <sarif_output_file>")
        sys.exit(0)

    pylint_json_file = sys.argv[1]
    sarif_output_file = sys.argv[2]

    print(f"Reading Pylint JSON from {pylint_json_file}...")
    print(f"Writing SARIF output to {sarif_output_file}...")
    with open(pylint_json_file, 'r') as f:
        pylint_json = json.load(f)

    sarif = convert_pylint_to_sarif(pylint_json)

    with open(sarif_output_file, 'w') as f:
        json.dump(sarif, f, indent=2)

    print(f"SARIF output written to {sarif_output_file}")

if __name__ == "__main__":
    main()