#!/usr/bin/env python3
import argparse
import configparser
import csv
import sys
import re
from pathlib import Path
from tcms_api import TCMS
from markdownify import markdownify as md

CONF_FILE = Path(__file__).parent / "tcms.conf"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    return (
        config.get("tcms", "url"),
        config.get("tcms", "username"),
        config.get("tcms", "password"),
    )


def has_html(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r"<[a-z][\s\S]*?>", text, re.IGNORECASE))


def html_to_markdown(html_content: str) -> str:
    if not html_content:
        return ""

    markdown_text = md(
        html_content,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )

    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
    # Collapse runs of non-breaking spaces left over from HTML
    markdown_text = markdown_text.replace("\xa0", " ")
    return markdown_text.strip()


def read_case_ids_from_csv(csv_path: str) -> list[int]:
    case_ids = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            case_ids.append(int(row["ID"]))
    return case_ids


def clean_kiwi_test_cases(
    target_case_id: int = None,
    csv_path: str = None,
    commit: bool = False,
):
    print("Connecting to Kiwi TCMS API...")
    try:
        url, username, password = load_config()
        rpc = TCMS(url, username, password).exec
    except Exception as e:
        print(f"Failed to connect to Kiwi TCMS API: {e}")
        sys.exit(1)

    if target_case_id:
        print(f"Fetching TestCase ID #{target_case_id}...")
        test_cases = rpc.TestCase.filter({"id": target_case_id})
        if not test_cases:
            print(f"Error: TestCase ID #{target_case_id} not found.")
            sys.exit(1)
    elif csv_path:
        case_ids = read_case_ids_from_csv(csv_path)
        print(f"Read {len(case_ids)} case ID(s) from {csv_path}")
        test_cases = rpc.TestCase.filter({"id__in": case_ids})
    else:
        print("Fetching all test cases...")
        test_cases = rpc.TestCase.filter({})

    print(f"Found {len(test_cases)} test case(s) to process.")
    converted_count = 0

    for case in test_cases:
        case_id = case.get("id")
        text_content = case.get("text", "")

        if not has_html(text_content):
            print(f"Skipping TestCase #{case_id}: no HTML detected.")
            continue

        converted_text = html_to_markdown(text_content)

        print(f"\n================ TestCase ID: {case_id} ================")
        if not commit:
            print(f"[DRY RUN] Original size: {len(text_content)} chars")
            print(f"[DRY RUN] Converted size: {len(converted_text)} chars")
            print("[DRY RUN] Markdown output:")
            print(converted_text)
        else:
            try:
                rpc.TestCase.update(case_id, {"text": converted_text})
                print(f"Updated TestCase #{case_id} ({len(text_content)} -> {len(converted_text)} chars)")
            except Exception as e:
                print(f"Error updating TestCase #{case_id}: {e}")

        converted_count += 1

    print("\n=========================================================")
    if not commit:
        print(f"Dry run complete ({converted_count} case(s) would be converted).")
        print("Re-run with --commit to apply changes to Kiwi TCMS.")
    else:
        print(f"Done! {converted_count} test case(s) converted to Markdown in Kiwi TCMS.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Kiwi TCMS test case HTML to Markdown."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "-c", "--case-id",
        type=int,
        help="Process a single TestCase ID.",
    )
    source.add_argument(
        "--csv",
        metavar="FILE",
        help="CSV exported from Kiwi TCMS (reads the ID column).",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Apply changes to Kiwi TCMS. Without this, runs in dry-run mode.",
    )

    args = parser.parse_args()
    clean_kiwi_test_cases(
        target_case_id=args.case_id,
        csv_path=args.csv,
        commit=args.commit,
    )
