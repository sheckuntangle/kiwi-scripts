#!/usr/bin/env python3
import configparser
import argparse
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
    parser.add_argument("product_id", type=int, help="Product ID")
    parser.add_argument("summary", help="Test Plan Summary")
    parser.add_argument("default_tester", help="Default tester")
    parser.add_argument("build", type=int, help="Build Version")
    parser.add_argument("manager", help="Manager")
    args = parser.parse_args()

    url, username, password = load_config()
    rpc = TCMS(url, username, password).exec

    values = {'summary': args.summary,
    'manager': args.manager,
    'default_tester': args.default_tester,
    'product': args.product_id,
    'plan': args.plan_id,
    'build': args.build,
    }

    rpc.TestRun.create(values)

if __name__ == "__main__":
    main()
