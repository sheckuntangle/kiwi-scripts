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
    parser = argparse.ArgumentParser(description="Add or remove a tag on Kiwi TCMS test cases")
    parser.add_argument("case_ids", type=int, nargs="+", help="One or more test case IDs")
    parser.add_argument("--tag", required=True, help="Tag name to add or remove")
    parser.add_argument("--remove", action="store_true", help="Remove the tag instead of adding it")
    args = parser.parse_args()

    url, username, password = load_config()
    rpc = TCMS(url, username, password)

    action = "remove_tag" if args.remove else "add_tag"
    verb = "Removed" if args.remove else "Added"

    for case_id in args.case_ids:
        try:
            getattr(rpc.exec.TestCase, action)(case_id, args.tag)
            print(f"{verb} tag '{args.tag}' on case {case_id}")
        except Exception as e:
            print(f"Failed to {action.replace('_', ' ')} '{args.tag}' on case {case_id}: {e}", file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main()
