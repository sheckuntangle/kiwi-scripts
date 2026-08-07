# kiwi-scripts

CLI utilities for bulk operations on [Kiwi TCMS](https://kiwitcms.org/) via the XML-RPC API.

## Setup

1. Install the Python client:

```bash
pip install tcms-api
```

2. Copy the example config and fill in your credentials:

```bash
cp tcms.conf.example tcms.conf
```

Edit `tcms.conf` with your Kiwi TCMS URL, username, and password (or API token).

## Scripts

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

## Configuration

All scripts read credentials from `tcms.conf` in the project root. See `tcms.conf.example` for the format. Do not commit `tcms.conf` — it contains credentials.
