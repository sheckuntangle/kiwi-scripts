#!/usr/bin/env python3
import argparse
import configparser
import sys
from pathlib import Path

from tcms_api import TCMS

CONF_FILE = Path(__file__).parent / "tcms.conf"
PRODUCT_NAME = "Velo"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    return (
        config.get("tcms", "url"),
        config.get("tcms", "username"),
        config.get("tcms", "password"),
    )


def section_name(value):
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("name must not be empty")
    return value


def add_section(rpc, kind, name):
    products = rpc.exec.Product.filter({"name": PRODUCT_NAME})
    if len(products) != 1:
        raise ValueError(f"Expected exactly one product named {PRODUCT_NAME}; found {len(products)}")
    product_id = products[0]["id"]
    api = getattr(rpc.exec, kind)
    existing = api.filter({"product": product_id, "name": name})
    if existing:
        print(f"{kind} {name!r} already exists under {PRODUCT_NAME} (ID: {existing[0]['id']})")
        return
    result = api.create({"product": product_id, "name": name})
    print(f"Created {kind.lower()} {name!r} under {PRODUCT_NAME} (ID: {result['id']})")


def main():
    parser = argparse.ArgumentParser(
        description="Create a component or category under the Velo product in Kiwi TCMS"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--component", type=section_name, metavar="NAME", help="Component to create")
    source.add_argument("--category", type=section_name, metavar="NAME", help="Category to create")
    args = parser.parse_args()
    kind = "Component" if args.component is not None else "Category"
    name = args.component if args.component is not None else args.category
    try:
        rpc = TCMS(*load_config())
        add_section(rpc, kind, name)
    except Exception as exc:
        print(f"Failed to create {kind.lower()} {name!r} under {PRODUCT_NAME}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
