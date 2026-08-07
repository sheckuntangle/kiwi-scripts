#!/usr/bin/env python3
import argparse
import configparser
import sys
from pathlib import Path
from tcms_api import TCMS

CONF_FILE = Path(__file__).parent / "tcms.conf"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    return (
        config.get("tcms", "url"),
        config.get("tcms", "username"),
        config.get("tcms", "password"),
    )


def main():
    parser = argparse.ArgumentParser(description="Set the automated status of Kiwi TCMS test cases")
    parser.add_argument("case_ids", type=int, nargs="+", help="One or more test case IDs")
    parser.add_argument("--status", choices=["true", "false"], required=True,
                        help="Set is_automated to true or false")
    args = parser.parse_args()

    is_automated = args.status == "true"
    url, username, password = load_config()
    rpc = TCMS(url, username, password)

    for case_id in args.case_ids:
        try:
            result = rpc.exec.TestCase.update(case_id, {"is_automated": is_automated})
            print(f"Case {case_id} ({result['summary']}): is_automated = {result['is_automated']}")
        except Exception as e:
            print(f"Failed to update case {case_id}: {e}", file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main()
