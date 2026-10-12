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
    return tuple(config.get("tcms", key) for key in ("url", "username", "password"))


def nonempty(value):
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("value must not be empty")
    return value


def lookup(api, query, label):
    matches = api.filter(query)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {label}; found {len(matches)}")
    return matches[0]


def create_test_case(rpc, product, category, component, title, priority="P2", status="CONFIRMED"):
    product_obj = lookup(rpc.exec.Product, {"name": product}, f"product {product!r}")
    scope = {"product": product_obj["id"]}
    category_obj = lookup(
        rpc.exec.Category, dict(scope, name=category), f"category {category!r} under {product!r}"
    )
    component_obj = lookup(
        rpc.exec.Component, dict(scope, name=component), f"component {component!r} under {product!r}"
    )
    priority_obj = lookup(rpc.exec.Priority, {"value": priority}, f"priority {priority!r}")
    status_obj = lookup(rpc.exec.TestCaseStatus, {"name": status}, f"status {status!r}")
    result = rpc.exec.TestCase.create({
        "category": category_obj["id"],
        "summary": title,
        "priority": priority_obj["id"],
        "case_status": status_obj["id"],
    })
    case_id = result["id"]
    try:
        rpc.exec.TestCase.add_component(case_id, component_obj["name"])
    except Exception as exc:
        raise RuntimeError(
            f"Test case {case_id} was created with title {title!r}, but attaching component "
            f"{component!r} failed: {exc}. Attach the component to this case manually; "
            "rerunning this script creates another test case."
        ) from exc
    print(f"Created test case {case_id}: {title!r} ({product} > {category} > {component})")
    return case_id


def main():
    parser = argparse.ArgumentParser(description="Create a Kiwi TCMS test case with a category and component")
    for option in ("product", "category", "component", "title"):
        help_text = "Test case title" if option == "title" else f"Existing {option} name"
        parser.add_argument(f"--{option}", required=True, type=nonempty, help=help_text)
    parser.add_argument("--priority", type=nonempty, default="P2", help="Priority value (default: P2)")
    parser.add_argument("--status", type=nonempty, default="CONFIRMED", help="Test case status name (default: CONFIRMED)")
    args = parser.parse_args()
    if len(args.title) > 255:
        parser.error("title must be at most 255 characters")
    try:
        create_test_case(TCMS(*load_config()), **vars(args))
    except Exception as exc:
        print(f"Failed to complete test case creation: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
