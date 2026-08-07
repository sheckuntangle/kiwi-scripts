# CLAUDE.md

## Project overview

CLI scripts for bulk operations on Kiwi TCMS using the `tcms-api` Python library and XML-RPC API.

## Scripts

- `add_cases_to_plan.py` — Links existing test cases to a test plan via `TestPlan.add_case(plan_id, case_id)`
- `set_automated.py` — Updates the `is_automated` field on test cases via `TestCase.update(case_id, values)`
- `convert_html2md.py` — Converts HTML content in test case `text` fields to Markdown via `TestCase.update(case_id, values)`. Accepts `--case-id` for a single case, `--csv` for a Kiwi TCMS CSV export (reads the `ID` column), or no filter to process all cases. Dry-run by default; pass `--commit` to apply changes. Depends on `markdownify`.
- `tag_cases.py` — Adds or removes a tag on test cases via `TestCase.add_tag(case_id, tag)` / `TestCase.remove_tag(case_id, tag)`. Pass `--remove` to remove instead of add.

## Configuration

- Scripts read connection details from `tcms.conf` (ini format, `[tcms]` section with `url`, `username`, `password`)
- `tcms.conf` is gitignored — use `tcms.conf.example` as a template
- Config loading is done via `configparser` using `Path(__file__).parent / "tcms.conf"`

## API reference

- Kiwi TCMS RPC docs: https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html
- `tcms-api` Python package: https://pypi.org/project/tcms-api/

## Commands

```bash
pip install tcms-api markdownify   # install dependencies
python add_cases_to_plan.py        # run with --help for usage
python set_automated.py            # run with --help for usage
python convert_html2md.py          # run with --help for usage
python tag_cases.py                # run with --help for usage
```
