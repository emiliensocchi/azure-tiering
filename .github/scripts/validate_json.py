"""
    Validates the syntax and structure of the JSON files in this repository.

    Checks performed:
        - Every *.json file in the repository is valid JSON without duplicate keys
        - tier_definitions.json defines names and definitions for each category
        - Tiered files contain well-formed assets, with tiers matching tier_definitions.json,
          the expected fields for each tier, and unique ids and asset names
        - Untiered files contain well-formed entries produced by AzTierWatcher

    Usage:
        python3 .github/scripts/validate_json.py

    Exits with a non-zero status code if any error is found.
"""
import datetime
import json
import os
import re
import sys


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TIER_DEFINITIONS_FILE = 'tier_definitions.json'

GUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
BASE_FIELDS = ('tier', 'id', 'assetName', 'assetDefinition', 'documentationUri')
PATH_FIELDS = ('pathType', 'shortestPath', 'example')
SCENARIO_FIELDS = ('shortestPath', 'example')

# For each category, maps a tier to the allowed sets of extra fields (in addition to BASE_FIELDS)
TIERED_FILES = {
    'azure': {
        'path': 'Azure roles/tiered-azure-roles.json',
        'tier_fields': {
            '0': [SCENARIO_FIELDS],
            '1': [SCENARIO_FIELDS],
            '2': [('worstCaseScenario',), SCENARIO_FIELDS],
            '3': [('worstCaseScenario',), SCENARIO_FIELDS],
        },
        'path_types': (),
    },
    'entra': {
        'path': 'Entra roles/tiered-entra-roles.json',
        'tier_fields': {
            '0': [PATH_FIELDS],
            '1': [('providesFullAccessTo',)],
            '2': [()],
        },
        'path_types': ('Direct', 'Indirect'),
    },
    'msgraph': {
        'path': 'Microsoft Graph application permissions/tiered-msgraph-app-permissions.json',
        'tier_fields': {
            '0': [PATH_FIELDS],
            '1': [()],
            '2': [()],
        },
        'path_types': ('Direct', 'Indirect', 'n/a'),
    },
}

UNTIERED_FILES = [
    'Entra roles/untiered-entra-roles.json',
    'Microsoft Graph application permissions/untiered-msgraph-app-permissions.json',
]
UNTIERED_FIELDS = ('detectedOn', 'apiEvent', 'id', 'assetName', 'assetDefinition', 'documentationUri')
UNTIERED_API_EVENTS = ('added', 'removed')


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs):
    """
        object_pairs_hook for json.load that fails on duplicate keys, which json silently overwrites by default.
    """
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key '{key}'")
        result[key] = value
    return result


def load_json(relative_path, errors):
    """
        Loads the passed JSON file, recording syntax errors and duplicate keys in the passed list.

        Returns:
            the parsed content, or None if the file could not be parsed
    """
    try:
        with open(os.path.join(ROOT_DIR, relative_path), 'r', encoding='utf-8') as file:
            return json.load(file, object_pairs_hook=reject_duplicate_keys)
    except FileNotFoundError:
        errors.append(f"{relative_path}: file not found")
    except UnicodeDecodeError as error:
        errors.append(f"{relative_path}: not valid UTF-8 ({error})")
    except json.JSONDecodeError as error:
        errors.append(f"{relative_path}: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}")
    except DuplicateKeyError as error:
        errors.append(f"{relative_path}: {error}")
    return None


def find_json_files():
    """
        Returns the relative paths of all JSON files in the repository.
    """
    json_files = []
    for dir_path, dir_names, file_names in os.walk(ROOT_DIR):
        dir_names[:] = [name for name in dir_names if name not in ('.git', 'node_modules')]
        for file_name in file_names:
            if file_name.lower().endswith('.json'):
                json_files.append(os.path.relpath(os.path.join(dir_path, file_name), ROOT_DIR).replace(os.sep, '/'))
    return sorted(json_files)


def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ''


def validate_tier_definitions(content, errors):
    """
        Validates tier_definitions.json and returns the tiers defined for each category, as {category: set(tiers)}.
    """
    defined_tiers = {}
    if not isinstance(content, dict):
        errors.append(f"{TIER_DEFINITIONS_FILE}: root must be an object")
        return defined_tiers

    for section in ('tier_names', 'tier_definitions'):
        if not isinstance(content.get(section), dict):
            errors.append(f"{TIER_DEFINITIONS_FILE}: missing or invalid '{section}' object")
            return defined_tiers

    for category in TIERED_FILES:
        section_tiers = []
        for section in ('tier_names', 'tier_definitions'):
            entries = content[section].get(category)
            if not isinstance(entries, dict) or not entries:
                errors.append(f"{TIER_DEFINITIONS_FILE}: missing or empty '{section}.{category}'")
                section_tiers.append(set())
                continue
            tiers = set()
            for key, value in entries.items():
                match = re.fullmatch(r'tier_(\d+)', key)
                if not match:
                    errors.append(f"{TIER_DEFINITIONS_FILE}: '{section}.{category}.{key}' must be named 'tier_<number>'")
                    continue
                if not is_non_empty_string(value):
                    errors.append(f"{TIER_DEFINITIONS_FILE}: '{section}.{category}.{key}' must be a non-empty string")
                tiers.add(match.group(1))
            section_tiers.append(tiers)

        if section_tiers[0] != section_tiers[1]:
            errors.append(f"{TIER_DEFINITIONS_FILE}: 'tier_names.{category}' and 'tier_definitions.{category}' define different tiers")
        defined_tiers[category] = section_tiers[0] | section_tiers[1]

    return defined_tiers


def validate_common_fields(location, asset, required_fields, errors):
    """
        Validates fields shared by tiered and untiered assets.
    """
    for field in required_fields:
        if field not in asset:
            errors.append(f"{location}: missing field '{field}'")
        elif not is_non_empty_string(asset[field]):
            errors.append(f"{location}: field '{field}' must be a non-empty string")

    if is_non_empty_string(asset.get('id')) and not GUID_REGEX.match(asset['id']):
        errors.append(f"{location}: 'id' is not a valid GUID ({asset['id']})")

    if is_non_empty_string(asset.get('documentationUri')) and not asset['documentationUri'].startswith('https://'):
        errors.append(f"{location}: 'documentationUri' must start with https:// ({asset['documentationUri']})")


def validate_tiered_file(category, content, defined_tiers, errors):
    """
        Validates the content of a tiered file.
    """
    config = TIERED_FILES[category]
    relative_path = config['path']

    if not isinstance(content, list):
        errors.append(f"{relative_path}: root must be an array")
        return

    if set(config['tier_fields']) != defined_tiers:
        errors.append(
            f"{relative_path}: validator expects tiers {sorted(config['tier_fields'])} but "
            f"{TIER_DEFINITIONS_FILE} defines {sorted(defined_tiers)} for '{category}' - update both together"
        )

    seen_ids = {}
    seen_names = {}
    for index, asset in enumerate(content):
        name = asset.get('assetName') if isinstance(asset, dict) else None
        location = f"{relative_path}[{index}]" + (f" ({name})" if name else '')

        if not isinstance(asset, dict):
            errors.append(f"{location}: entry must be an object")
            continue

        validate_common_fields(location, asset, BASE_FIELDS, errors)

        tier = asset.get('tier')
        if is_non_empty_string(tier) and tier not in defined_tiers:
            errors.append(f"{location}: tier '{tier}' is not defined for '{category}' in {TIER_DEFINITIONS_FILE}")

        allowed_variants = config['tier_fields'].get(tier)
        if allowed_variants is not None:
            extra_fields = set(asset) - set(BASE_FIELDS)
            if not any(extra_fields == set(variant) for variant in allowed_variants):
                expected = ' or '.join(str(sorted(variant)) for variant in allowed_variants)
                errors.append(f"{location}: tier {tier} expects extra fields {expected}, found {sorted(extra_fields)}")
            for field in extra_fields:
                if not is_non_empty_string(asset[field]):
                    errors.append(f"{location}: field '{field}' must be a non-empty string")

        if 'pathType' in asset and config['path_types'] and asset['pathType'] not in config['path_types']:
            errors.append(f"{location}: 'pathType' must be one of {list(config['path_types'])}, found '{asset['pathType']}'")

        asset_id = asset.get('id')
        if isinstance(asset_id, str):
            key = asset_id.lower()
            if key in seen_ids:
                errors.append(f"{location}: duplicate id '{asset_id}' (also at index {seen_ids[key]})")
            else:
                seen_ids[key] = index

        if isinstance(name, str):
            if name in seen_names:
                errors.append(f"{location}: duplicate assetName '{name}' (also at index {seen_names[name]})")
            else:
                seen_names[name] = index


def validate_untiered_file(relative_path, content, errors):
    """
        Validates the content of an untiered file, as written by AzTierWatcher.
    """
    if not isinstance(content, list):
        errors.append(f"{relative_path}: root must be an array")
        return

    seen_ids = {}
    for index, asset in enumerate(content):
        location = f"{relative_path}[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{location}: entry must be an object")
            continue

        validate_common_fields(location, asset, UNTIERED_FIELDS, errors)

        unexpected_fields = set(asset) - set(UNTIERED_FIELDS)
        if unexpected_fields:
            errors.append(f"{location}: unexpected fields {sorted(unexpected_fields)}")

        if is_non_empty_string(asset.get('apiEvent')) and asset['apiEvent'] not in UNTIERED_API_EVENTS:
            errors.append(f"{location}: 'apiEvent' must be one of {list(UNTIERED_API_EVENTS)}, found '{asset['apiEvent']}'")

        if is_non_empty_string(asset.get('detectedOn')):
            try:
                datetime.datetime.strptime(asset['detectedOn'], '%Y-%m-%d')
            except ValueError:
                errors.append(f"{location}: 'detectedOn' must be a YYYY-MM-DD date, found '{asset['detectedOn']}'")

        asset_id = asset.get('id')
        if isinstance(asset_id, str):
            key = asset_id.lower()
            if key in seen_ids:
                errors.append(f"{location}: duplicate id '{asset_id}' (also at index {seen_ids[key]})")
            else:
                seen_ids[key] = index


def main():
    errors = []
    parsed = {}

    # Syntax: every JSON file in the repository must parse
    json_files = find_json_files()
    for relative_path in json_files:
        parsed[relative_path] = load_json(relative_path, errors)

    # Structure: known data files
    for relative_path in [TIER_DEFINITIONS_FILE] + [config['path'] for config in TIERED_FILES.values()] + UNTIERED_FILES:
        if relative_path not in parsed:
            errors.append(f"{relative_path}: file not found")

    tier_definitions = parsed.get(TIER_DEFINITIONS_FILE)
    defined_tiers = validate_tier_definitions(tier_definitions, errors) if tier_definitions is not None else {}

    for category, config in TIERED_FILES.items():
        content = parsed.get(config['path'])
        if content is not None and category in defined_tiers:
            validate_tiered_file(category, content, defined_tiers[category], errors)

    for relative_path in UNTIERED_FILES:
        content = parsed.get(relative_path)
        if content is not None:
            validate_untiered_file(relative_path, content, errors)

    if errors:
        for error in errors:
            print(f"::error::{error}" if os.environ.get('GITHUB_ACTIONS') else f"ERROR: {error}")
        print(f"\nFAILED - {len(errors)} error(s) found in {len(json_files)} JSON file(s)")
        return 1

    print(f"OK - {len(json_files)} JSON file(s) are valid")
    return 0


if __name__ == '__main__':
    sys.exit(main())
