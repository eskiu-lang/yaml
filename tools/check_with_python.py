#!/usr/bin/env python3
"""Checks the expected values in tests/yaml.esk against ruamel.yaml (YAML 1.2, core schema).

    python3 -m pip install ruamel.yaml
    python3 -I tools/check_with_python.py

Each ok("yaml", "json") case is loaded by ruamel and compared with the expected JSON
(infinities and NaN compare as null, as JsonValue_stringify writes them); each bad(...)
case must make ruamel fail too, except the ones listed in ALLOWED, which ruamel accepts
but this package leaves out on purpose. KNOWN lists the cases where ruamel departs from
the YAML 1.2 spec.
"""
import ast
import io
import json
import math
import re
import sys

from ruamel.yaml import YAML

ALLOWED = ("anchors and aliases", "tags", "directives", "complex keys", "several documents",
           "flow sequence")

# Cases where this package follows the YAML 1.2 spec and ruamel does not.
KNOWN = {
    "1_000": "the core schema's integers have no '_' (ruamel reads 1000)",
    "1: one\ntrue: t\n": "keys are strings here; in Python 1 and True are the same key",
    "a:\tb\n": "a tab may separate the value from ':' (YAML 1.2 s-separate-in-line)",
}

src = open("tests/yaml.esk", encoding="utf-8").read()


def c_string(lit):
    body = lit[1:-1]
    out = bytearray()
    i = 0
    while i < len(body):
        c = body[i]
        if c != "\\":
            out += c.encode()
            i += 1
            continue
        e = body[i + 1]
        if e == "x":
            m = re.match(r"[0-9a-fA-F]{1,2}", body[i + 2:])
            out.append(int(m.group(0), 16) & 0xFF)
            i += 2 + len(m.group(0))
            continue
        out += {"n": b"\n", "t": b"\t", "r": b"\r", "\\": b"\\", '"': b'"', "'": b"'"}[e]
        i += 2
    return out.decode("utf-8")


def norm(v):
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
        return None
    if isinstance(v, float) and v == int(v) and abs(v) < 2**53:
        return int(v)
    if isinstance(v, dict):
        return {str(k).lower() if isinstance(k, bool) else str(k): norm(x) for k, x in v.items()}
    if isinstance(v, list):
        return [norm(x) for x in v]
    return v


def load(text):
    y = YAML(typ="safe", pure=True)
    y.version = (1, 2)
    return y.load(io.StringIO(text))


STR = r'"(?:[^"\\]|\\.)*"'
bad_count = 0
n = 0
for m in re.finditer(r'\bok\(\s*(' + STR + r'(?:\s*' + STR + r')*)\s*,\s*(' + STR + r')\s*\);', src):
    parts = re.findall(STR, m.group(1))
    text = "".join(c_string(p) for p in parts)
    want = json.loads(c_string(m.group(2)))
    n += 1
    if text in KNOWN:
        continue
    try:
        got = norm(load(text.lstrip("﻿")))
    except Exception as e:
        print(f"ruamel rejects {text!r}: {e}")
        bad_count += 1
        continue
    if got != norm(want):
        print(f"differs {text!r}: ruamel {got!r}, expected {want!r}")
        bad_count += 1
for m in re.finditer(r'\bbad\(\s*(' + STR + r')\s*,\s*\d+\s*,\s*\d+\s*,\s*(' + STR + r')\s*\);', src):
    text = c_string(m.group(1))
    msg = c_string(m.group(2))
    n += 1
    try:
        load(text)
    except Exception:
        continue
    if any(a in msg for a in ALLOWED):
        continue
    print(f"ruamel accepts {text!r}, the test expects an error ({msg})")
    bad_count += 1
print(f"{n} cases, {bad_count} differences")
sys.exit(1 if bad_count else 0)
