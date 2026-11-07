# yaml documentation

Guides and reference for yaml. The [README](../README.md) has the overview.

<!-- pages -->
- [API reference](api.md): every public function and type
<!-- /pages -->

## What is left out

Anchors and aliases (`&a`, `*a`), tags (`!x`), complex keys (`? `), directives
(`%YAML`), several documents in one stream and a `key: value` pair inside a flow sequence
are each reported as an error at their position. Tabs may separate tokens but not indent.
Numbers are doubles, as in `<json>`, so an integer past 2^53 loses precision, and keys are
always strings (`1: a` has the key `"1"`).

## Contributing

Bug reports are welcome; please include the YAML and the `eskiuc --version` output. The
tests run with `eskiuc test`. `python3 -I tools/check_with_python.py` (with
`pip install ruamel.yaml`) compares the tests' expected values with ruamel.yaml, and
`python3 -I tools/gen_api.py` regenerates `docs/api.md` from the source comments.
