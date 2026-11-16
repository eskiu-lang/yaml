# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-11-16

### Changed

- The package moved to the eskiu-packages organization; the old URL redirects. The sources are split into files by topic. No API change.

## [0.1.0]

### Added

- `yaml_parse`, `yaml_parse_bytes` and `yaml_load`: one YAML document into a `<json>`
  `JsonValue` under the YAML 1.2 core schema, with block and flow collections, every scalar
  style and comments; `YamlError` with the line, column and reason of a failure.
