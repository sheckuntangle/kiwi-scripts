# kiwi-scripts

CLI utilities for bulk operations on [Kiwi TCMS](https://kiwitcms.org/) via the XML-RPC API.

## Setup

1. Install the Python client:

```bash
pip install tcms-api markdownify
```

2. Copy the example config and fill in your credentials:

```bash
cp tcms.conf.example tcms.conf
```

Edit `tcms.conf` with your Kiwi TCMS URL, username, and password (or API token).

## Scripts

### create_test_case.py

Create a test case with a title, category, and component in any existing product:

```bash
python3 create_test_case.py --product "Velo" --category "High Availability" \
    --component "HA Policy Management" --title "Verify HA policy creation"
```

All four options are required and accept names (the title becomes Kiwi's `summary`). The category and component must belong to the selected product. Names must match exactly; missing or ambiguous matches stop creation. Titles must be nonempty and at most 255 characters.

Kiwi also requires priority and status. Defaults are `--priority "P2"` and `--status "CONFIRMED"`; override them with existing priority values and status names when needed. The configured user becomes the author. The case description is empty and the case is not added to a test plan.

The script writes immediately and prints the new case ID, title, and `product > category > component` association. Categories and components both belong directly to the product. Every invocation creates a new case, even if its title already exists. Component attachment is a separate API call: if it fails after creation, the script exits nonzero and reports the created case ID for manual recovery. Do not rerun to repair attachment, as that creates another case. Use `python3 create_test_case.py --help` for all options.

### add_case_section.py

Create a component or category for test cases under **Velo**. Supply exactly one of `--component` or `--category`; the product is always Velo.

```bash
python3 add_case_section.py --component <name>
python3 add_case_section.py --category <name>
```

**Examples:**

```bash
python3 add_case_section.py --category "High Availability"
python3 add_case_section.py --component "HA Policy Management"
python3 add_case_section.py --help
```

The script writes immediately. If the named component or category already exists under Velo, it reports its ID without creating a duplicate. It requires exactly one existing product named Velo and exits with a nonzero status on failure. Creating a section does not assign it to existing test cases.

Categories and components both belong directly to the product in Kiwi; components are not nested under categories. A test case can use the **High Availability** category alongside the **HA Policy Management** component. Quote names containing spaces. The script uses the same `tcms.conf` credentials as the other utilities.

### add_cases_to_plan.py

Add one or more existing test cases to a test plan.

```bash
python add_cases_to_plan.py <plan_id> <case_id> [case_id ...]
```

**Example:**

```bash
python add_cases_to_plan.py 25 7273 7274 7275 7276
```

### set_automated.py

Set the `is_automated` flag on one or more test cases.

```bash
python set_automated.py --status <true|false> <case_id> [case_id ...]
```

**Examples:**

```bash
# Mark cases as automated
python set_automated.py --status true 7273 7274 7275

# Mark cases as not automated
python set_automated.py --status false 7273 7274 7275
```

### convert_html2md.py

Convert HTML content in test case descriptions to clean Markdown. Runs in dry-run mode by default — use `--commit` to apply changes to Kiwi TCMS.

```bash
# Dry-run a single test case
python convert_html2md.py -c 7273

# Apply changes to a single test case
python convert_html2md.py -c 7273 --commit

# Process cases from a Kiwi TCMS CSV export (dry-run)
python convert_html2md.py --csv "Kiwi TCMS - Search Test Cases.csv"

# Apply changes from a CSV export
python convert_html2md.py --csv "Kiwi TCMS - Search Test Cases.csv" --commit

# Dry-run all test cases (preview only)
python convert_html2md.py

# Apply changes to all test cases
python convert_html2md.py --commit
```

The `--csv` option reads the `ID` column from a CSV exported via Kiwi TCMS's search results page. This is useful for targeting a specific set of test cases without processing every case in the system.

### tag_cases.py

Add or remove a tag on one or more test cases.

```bash
python tag_cases.py --tag <tag_name> <case_id> [case_id ...]
```

**Examples:**

```bash
# Add a tag
python tag_cases.py --tag "regression" 7273 7274 7275

# Remove a tag
python tag_cases.py --tag "regression" --remove 7273 7274 7275
```

## Configuration

All scripts read credentials from `tcms.conf` in the project root. See `tcms.conf.example` for the format. Do not commit `tcms.conf` — it contains credentials.
