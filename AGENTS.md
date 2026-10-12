# Repository guidance

## Purpose and layout

This repository contains standalone Python CLI utilities for maintaining test cases in Kiwi TCMS through the `tcms-api` client and XML-RPC API. Read `README.md` for user-facing usage and `CLAUDE.md` for the existing companion guidance. Keep these documents consistent with changes to scripts.

| Script | Behavior |
| --- | --- |
| `create_test_case.py` | Resolves product/category/component names, creates a titled case with `TestCase.create(values)`, then attaches a component by name with `TestCase.add_component(case_id, component_name)`. Defaults priority/status to P2/CONFIRMED. |
| `add_case_section.py` | Creates a component or category under Velo using `Component.create(values)` or `Category.create(values)`; requires mutually exclusive `--component`/`--category`, skips existing names, and exits nonzero on failure. |
| `add_cases_to_plan.py` | Links existing cases to a plan using `TestPlan.add_case(plan_id, case_id)`. |
| `set_automated.py` | Sets `is_automated` using `TestCase.update(case_id, values)`; requires `--status true` or `--status false`. |
| `tag_cases.py` | Calls `TestCase.add_tag` by default or `TestCase.remove_tag` with `--remove`; requires `--tag`. |
| `convert_html2md.py` | Fetches cases with `TestCase.filter`, converts HTML in their `text` fields with `markdownify`, and writes with `TestCase.update` only when `--commit` is supplied. |

There is currently no package structure, dependency manifest, test suite, or configured lint/build workflow. Keep changes proportional to this small script-based repository.

## Dependencies and configuration

- Use Python 3.9 or newer; the converter uses `list[int]` annotations.
- External dependencies are `tcms-api` and `markdownify`. Prefer an isolated environment when installation is needed: `python3 -m pip install tcms-api markdownify`.
- Every script loads `tcms.conf` relative to its own location with `Path(__file__).parent / "tcms.conf"`, rather than relative to the working directory. Preserve this behavior.
- `tcms.conf.example` documents the INI format: a `[tcms]` section containing `url`, `username`, and `password`. The password may be an API token.
- `tcms.conf` is ignored by Git and contains credentials. Use the example for development guidance; do not print, copy into documentation, or commit real credentials. Use placeholders in examples and test fixtures.

## Working conventions

- Follow the existing `argparse`, `configparser`, `pathlib`, and `TCMS` patterns. Keep imports and reusable functions safe to load without invoking the CLI.
- Preserve existing argument names, required arguments, integer ID parsing, and API method signatures unless the requested change requires otherwise.
- Preserve per-case progress reporting and the ability to continue a bulk operation after an individual case fails. Report failures clearly; avoid claiming a successful batch solely from its exit code or final summary.
- The converter accepts mutually exclusive `--case-id`/`-c` and `--csv` sources. Without either, it fetches all cases. CSV input uses the `ID` column and `utf-8-sig` encoding to support an exported UTF-8 BOM.
- Preserve the converter's default dry run and explicit `--commit` write flag. Conversion currently uses ATX headings, `-` bullets, `markdownify`'s `strip=["script", "style"]` option, collapsed excess blank lines, normalized non-breaking spaces, and trimmed output.
- Update `README.md` when adding scripts, dependencies, or changing CLI behavior. Update agent guidance when repository workflows change.
- Avoid unrelated refactoring or introducing a framework for a narrowly scoped maintenance task.

## Remote operations

- `create_test_case.py` writes immediately and creates a new case on every invocation. If component attachment fails, it reports the created case ID and exits nonzero; rerunning creates a duplicate rather than repairing attachment.
- `add_case_section.py` writes immediately when the requested component or category does not already exist under Velo. It does not assign sections to test cases.
- `add_cases_to_plan.py`, `set_automated.py`, and `tag_cases.py` write immediately when invoked with valid arguments. They have no dry-run option.
- `convert_html2md.py` connects to Kiwi and reads cases even in dry-run mode. With `--commit` and no source filter, it can modify every case containing detected HTML.
- For code or documentation work, validate locally without contacting Kiwi. Run live operations only when the user's request authorizes the operation and target scope; honor authorization already given in the conversation.
- When performing an authorized conversion, preview the intended cases before committing and use explicit case IDs or a scoped CSV when appropriate.

## Validation

For Python changes, syntax-check without importing dependencies, loading credentials, or contacting Kiwi:

```bash
python3 - <<'PY'
import ast
from pathlib import Path
for path in Path('.').glob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    print(f'OK: {path}')
PY
```

With dependencies installed, `python3 <script>.py --help` checks argument parsing without loading configuration or creating a client in the current scripts. Do not run a script with operational arguments as a smoke test.

For behavior changes, use focused local checks or tests with a mocked `TCMS` client and temporary CSV/config fixtures. Check the affected API arguments, case selection, failure handling, and whether writes occur. For conversion changes, include representative HTML and existing plain text/Markdown, and verify that dry-run mode never calls `TestCase.update`. No new tests are needed solely for documentation changes.

Before finishing, review `git diff --check` and the diff for unintended changes or credentials. Report what was validated and any checks that could not run.

## API references

- Kiwi TCMS RPC API: https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html
- Python client: https://pypi.org/project/tcms-api/
