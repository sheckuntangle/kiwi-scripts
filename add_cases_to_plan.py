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
    parser = argparse.ArgumentParser(description="Add test cases to a Kiwi TCMS test plan")
    parser.add_argument("plan_id", type=int, help="Test plan ID")
    parser.add_argument("case_ids", type=int, nargs="+", help="One or more test case IDs")
    args = parser.parse_args()

    url, username, password = load_config()
    rpc = TCMS(url, username, password)

    for case_id in args.case_ids:
        try:
            result = rpc.exec.TestPlan.add_case(args.plan_id, case_id)
            print(f"Added case {case_id} to plan {args.plan_id} (sortkey: {result.get('sortkey', 'N/A')})")
        except Exception as e:
            print(f"Failed to add case {case_id} to plan {args.plan_id}: {e}", file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main()
