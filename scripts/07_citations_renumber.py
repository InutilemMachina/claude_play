"""
citations_renumber.py -- Fix query-local [N] citation numbers in assembled Jegyzet.

Problem: NLM CLI restarts citation numbering at [1] for every query. When multiple
query answers are assembled into one Jegyzet.md, inline <sup>[N]</sup> references
are ambiguous.

Solution (B option):
  1. Read citations.json       -- uuid -> global_number
  2. For each nlm_q*_raw.txt   -- local_N -> uuid (per query)
  3. Build local_N -> global_N per query
  4. Apply replacements using <!-- Q:N --> section markers (preferred)
     or unanimous-only fallback (no markers)

Usage:
    python scripts/citations_renumber.py --het 1 --tantargy matrixprofil_teszt
    python scripts/citations_renumber.py --het 1 --tantargy matrixprofil_teszt --dry-run
"""

import argparse
import json
import re
import shutil
from pathlib import Path


# ---------------------------------------------------------------------------
# Load helpers
# ---------------------------------------------------------------------------

def load_citations_json(path):
    """Load citations.json. Returns {uuid: global_num (int)}."""
    with open(path, encoding='utf-8') as f:
        raw = json.load(f)
    uuid_to_global = {}
    for key, val in raw.items():
        if key.startswith('_'):
            continue
        if isinstance(val, dict) and 'nlm_uuid' in val:
            uuid_to_global[val['nlm_uuid']] = int(key)
    return uuid_to_global


def load_query_file(path):
    """
    Load one NLM raw query JSON.
    Returns {'answer': str, 'local_citations': {local_N_str: uuid_str}}.
    """
    with open(path, encoding='utf-8-sig') as f:
        raw = json.load(f)
    val = raw.get('value', raw)
    return {
        'answer': val.get('answer', ''),
        'local_citations': val.get('citations', {}),
    }


def build_local_to_global(local_cits, uuid_to_global):
    """
    Build local_N -> global_N for one query.
    local_cits: {"1": "uuid-a", "2": "uuid-b", ...}
    Returns: {"1": 1, "2": 4, ...}  -- None for unknown UUIDs.
    """
    return {
        local_n: uuid_to_global.get(uuid, None)
        for local_n, uuid in local_cits.items()
    }


# ---------------------------------------------------------------------------
# Replacement logic
# ---------------------------------------------------------------------------

def replace_citations_in_text(text, local_to_global):
    """
    Replace <sup>[N]</sup> and <sup>[N, M, ...]</sup> using local->global map.
    Returns (modified_text, n_replacements).
    """
    count = [0]

    def repl(m):
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(',')]
        new_parts = []
        changed = False
        for p in parts:
            gn = local_to_global.get(p)
            if gn is not None and str(gn) != p:
                new_parts.append(str(gn))
                changed = True
            else:
                new_parts.append(p)
        if changed:
            count[0] += 1
        return '<sup>[' + ', '.join(new_parts) + ']</sup>'

    text = re.sub(r'<sup>\[([0-9, ]+)\]</sup>', repl, text)
    return text, count[0]


def apply_by_section_markers(text, query_maps):
    """
    Split on <!-- Q:N --> markers, apply per-query map, reassemble.
    Returns (modified_text, counts_list).
    """
    marker_re = re.compile(r'(<!-- Q:(\d+) -->)')
    parts = marker_re.split(text)

    if len(parts) == 1:
        return text, []

    result = [parts[0]]
    counts = []
    i = 1
    while i < len(parts):
        marker = parts[i]
        q_str = parts[i + 1]
        section = parts[i + 2]
        q_idx = int(q_str) - 1
        if 0 <= q_idx < len(query_maps):
            new_section, n = replace_citations_in_text(section, query_maps[q_idx])
            counts.append(n)
        else:
            new_section = section
            counts.append(0)
        result.extend([marker, q_str, new_section])
        i += 3

    return ''.join(result), counts


def apply_fallback_unanimous(text, query_maps):
    """
    Fallback (no section markers): only applies mappings where ALL queries agree.
    Ambiguous mappings (different global_N for same local_N) are skipped.
    Returns (modified_text, n_replacements).
    """
    all_maps = {}
    for qmap in query_maps:
        for local_n, global_n in qmap.items():
            if global_n is None:
                continue
            all_maps.setdefault(local_n, set()).add(global_n)

    unanimous = {}
    ambiguous = []
    for local_n, gset in all_maps.items():
        if len(gset) == 1:
            unanimous[local_n] = next(iter(gset))
        else:
            ambiguous.append('  [' + local_n + '] -> ' + str(sorted(gset)) + ' (skipped)')

    if ambiguous:
        print('WARN: ambiguous citations (no Q:N markers) -- skipped:')
        for a in ambiguous:
            print(a)
        print('  Fix: add <!-- Q:N --> markers via 01_nlm_query_runner.')
        print('  Applying only ' + str(len(unanimous)) + ' unambiguous mappings.')

    return replace_citations_in_text(text, unanimous)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Fix query-local citations in Jegyzet.md')
    parser.add_argument('--het', required=True, help='Week number (e.g. 1)')
    parser.add_argument('--tantargy', required=True, help='Subject folder path')
    parser.add_argument('--dry-run', action='store_true', help='Show changes, do not write')
    args = parser.parse_args()

    n = args.het
    base = Path(args.tantargy) / (n + '_het')
    forrasok = base / 'forrasok'
    citations_path = forrasok / 'citations.json'
    jegyzet_path = base / (n + '_Jegyzet.md')

    if not citations_path.exists():
        print('Hianyzik: ' + str(citations_path))
        return
    if not jegyzet_path.exists():
        print('Hianyzik: ' + str(jegyzet_path))
        return

    uuid_to_global = load_citations_json(citations_path)
    print('citations.json: ' + str(len(uuid_to_global)) + ' source(s)')

    query_files = sorted(forrasok.glob('nlm_q*_raw.txt'))
    if not query_files:
        query_files = sorted(forrasok.glob('nlm_q*.txt'))
    print('Query files: ' + str([f.name for f in query_files]))

    query_maps = []
    for qf in query_files:
        qdata = load_query_file(qf)
        lmap = build_local_to_global(qdata['local_citations'], uuid_to_global)
        query_maps.append(lmap)
        n_unk = sum(1 for v in lmap.values() if v is None)
        print('  ' + qf.name + ': ' + str(len(lmap)) + ' citations, ' + str(n_unk) + ' unknown UUID(s)')

    with open(str(jegyzet_path), encoding='utf-8') as f:
        text = f.read()

    has_markers = bool(re.search(r'<!-- Q:\d+ -->', text))
    if has_markers:
        print('\nSection markers found -- applying per-query replacement...')
        new_text, counts = apply_by_section_markers(text, query_maps)
        total = sum(counts)
        print('Total: ' + str(total) + ' replacements ' + str(counts))
    else:
        print('\nWARN: no <!-- Q:N --> markers -- unanimous fallback...')
        new_text, total = apply_fallback_unanimous(text, query_maps)
        print('Total: ' + str(total) + ' replacements')

    if args.dry_run:
        print('\n[DRY RUN] Changed lines:')
        old_lines = text.splitlines()
        new_lines = new_text.splitlines()
        for i, (o, nu) in enumerate(zip(old_lines, new_lines)):
            if o != nu:
                print('  L' + str(i + 1) + ': ' + repr(o) + '  ->  ' + repr(nu))
        return

    bak_path = str(jegyzet_path) + '.bak'
    shutil.copy2(str(jegyzet_path), bak_path)
    with open(str(jegyzet_path), 'w', encoding='utf-8') as f:
        f.write(new_text)

    print('\nOK: ' + str(total) + ' replacements written to ' + str(jegyzet_path))
    print('   Backup: ' + bak_path)


if __name__ == '__main__':
    main()
