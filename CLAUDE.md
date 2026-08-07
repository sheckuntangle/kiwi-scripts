# CLAUDE.md

## Project overview

CLI scripts for bulk operations on Kiwi TCMS using the `tcms-api` Python library and XML-RPC API.

## Scripts

- `add_cases_to_plan.py` — Links existing test cases to a test plan via `TestPlan.add_case(plan_id, case_id)`
- `set_automated.py` — Updates the `is_automated` field on test cases via `TestCase.update(case_id, values)`

## Configuration

- Scripts read connection details from `tcms.conf` (ini format, `[tcms]` section with `url`, `username`, `password`)
- `tcms.conf` is gitignored — use `tcms.conf.example` as a template
- Config loading is done via `configparser` using `Path(__file__).parent / "tcms.conf"`

## API reference

- Kiwi TCMS RPC docs: https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html
- `tcms-api` Python package: https://pypi.org/project/tcms-api/

## Commands

```bash
pip install tcms-api          # install dependency
python add_cases_to_plan.py   # run with --help for usage
python set_automated.py       # run with --help for usage
```
