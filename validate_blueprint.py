#!/usr/bin/env python3
"""Validate HA blueprint YAML against schema rules (from blueprint-schema-checklist.md)."""
import yaml
import sys
from pathlib import Path

VALID_DOMAINS = ('automation', 'script', 'template')
VALID_SELECTORS = (
    'action', 'app', 'area', 'attribute', 'assist_pipeline',
    'backup_location', 'boolean', 'choose', 'color_temperature',
    'condition', 'config_entry', 'constant', 'conversation_agent',
    'country', 'date', 'datetime', 'device', 'duration', 'entity',
    'floor', 'icon', 'label', 'language', 'location', 'media',
    'number', 'object', 'qr_code', 'rgb_color', 'select',
    'state', 'statistic', 'target', 'template', 'text',
    'theme', 'time', 'trigger'
)
VALID_MODES = ('single', 'queued', 'parallel', 'restart')

def check_input(key, val, path_hint=""):
    """Validate a single input definition."""
    if val is None:
        print(f"WARNING: input '{key}' has NO config (bare name) in {path_hint}")
        return

    if not isinstance(val, dict):
        print(f"ERROR: input '{key}' is not a dict/map in {path_hint}")
        return

    # Check for section (has 'input' sub-key)
    if 'input' in val:
        section_inputs = val.get('input', {})
        if not isinstance(section_inputs, dict):
            print(f"ERROR: Section '{key}' .input is not a dict")
        else:
            for inp_key, inp_val in section_inputs.items():
                check_input(inp_key, inp_val, f"section '{key}'")
        # Check collapsed rule
        if val.get('collapsed') is True:
            for inp_key, inp_val in section_inputs.items():
                if isinstance(inp_val, dict) and 'default' not in inp_val:
                    print(f"ERROR: Input '{inp_key}' in collapsed section '{key}' has no default")
        return

    # Regular input
    sel = val.get('selector')
    if sel:
        if not isinstance(sel, dict) or len(sel) != 1:
            print(f"ERROR: Input '{key}' selector must be a dict with exactly 1 key in {path_hint}")
        else:
            sel_type = list(sel.keys())[0]
            if sel_type not in VALID_SELECTORS:
                print(f"ERROR: Invalid selector '{sel_type}' in input '{key}' in {path_hint}")

    # Check default type vs selector
    if 'default' in val and sel:
        default_val = val['default']
        sel_type = list(sel.keys())[0] if isinstance(sel, dict) and len(sel) == 1 else None
        sel_opts = list(sel.values())[0] if sel_type else {}

        if sel_type == 'boolean' and not isinstance(default_val, bool):
            print(f"ERROR: Input '{key}' default must be boolean for boolean selector, got {type(default_val).__name__}")
        if sel_type == 'select' and isinstance(sel_opts, dict):
            if sel_opts.get('multiple') is True and not isinstance(default_val, list):
                print(f"ERROR: Input '{key}' default must be a list for multi-select")
            if not sel_opts.get('multiple') and not isinstance(default_val, str):
                print(f"ERROR: Input '{key}' default must be a string for single-select")
        if sel_type == 'entity' and isinstance(sel_opts, dict):
            if sel_opts.get('multiple') is True and not isinstance(default_val, list):
                print(f"ERROR: Input '{key}' default must be a list for multi-entity")
        if sel_type == 'number' and not isinstance(default_val, (int, float)):
            print(f"ERROR: Input '{key}' default must be numeric for number selector")


def check(path):
    with open(path) as f:
        data = yaml.safe_load(f)

    issues = []

    # 1. blueprint block exists
    bp = data.get('blueprint')
    if bp is None:
        issues.append("MISSING 'blueprint:' block")
        return issues

    # 2. name
    if not isinstance(bp.get('name'), str) or not bp['name'].strip():
        issues.append("MISSING or empty 'blueprint.name'")

    # 3. domain
    domain = bp.get('domain')
    if domain not in VALID_DOMAINS:
        issues.append(f"INVALID or MISSING domain: '{domain}'")

    # 4. description
    if not bp.get('description'):
        print("  ℹ Optional: no 'description' field")

    # 5. input
    # For script domain, inputs are handled differently (fields vs blueprint.input)
    # Our blueprint uses 'fields' at top level (script-level), NOT blueprint.input
    inputs = bp.get('input')
    if inputs is not None:
        if not isinstance(inputs, dict):
            issues.append("'blueprint.input' must be a dict")
        else:
            for key, val in inputs.items():
                check_input(key, val)
    else:
        print("  ℹ No 'blueprint.input' — inputs handled via script-level fields")

    # 6. Check top-level keys for script domain
    if domain == 'script':
        if 'sequence' not in data:
            issues.append("MISSING 'sequence:' at top level (required for script blueprints)")

        # Check mode
        mode = data.get('mode')
        if mode is not None and mode not in VALID_MODES:
            issues.append(f"INVALID mode: '{mode}'")

        # Check max_exceeded only valid with restart
        if 'max_exceeded' in data and data.get('mode') != 'restart':
            issues.append("'max_exceeded' requires mode: restart")

        # fields placement check: fields must NOT be under blueprint:
        if 'fields' in bp:
            issues.append("'fields' found under 'blueprint:' — must be at top level for script domain")

        # Validate top-level fields
        fields = data.get('fields')
        if fields:
            if not isinstance(fields, dict):
                issues.append("'fields' must be a map")
            else:
                for key, val in fields.items():
                    check_input(key, val, "top-level fields")

        # Check variables placement
        if 'variables' in bp:
            issues.append("'variables' found under 'blueprint:' — must be at top level")

    # 7. homeassistant min_version format
    ha = bp.get('homeassistant')
    if ha and 'min_version' in ha:
        v = ha['min_version']
        parts = str(v).split('.')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            issues.append(f"min_version '{v}' must be X.Y.Z format with 3 numeric parts")

    # Report
    if issues:
        for iss in issues:
            print(f"  FAIL: {iss}")
    else:
        print(f"  PASS: {path}")

    return len(issues) == 0


if __name__ == '__main__':
    all_ok = True
    for p in sys.argv[1:]:
        print(f"--- {p} ---")
        if not Path(p).exists():
            print(f"  MISSING file: {p}")
            all_ok = False
            continue
        ok = check(p)
        if not ok:
            all_ok = False
    sys.exit(0 if all_ok else 1)