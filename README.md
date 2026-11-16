<p align="center">
  <img src="https://raw.githubusercontent.com/eskiu-lang/eskiu/main/assets/logo.png" alt="Eskiu, a kitten with a ball of yarn" width="140">
</p>

<h2 align="center">yaml</h2>
<p align="center">YAML configuration files for Eskiu, read into the standard library's JSON tree.</p>
<p align="center"><sub>Part of the <a href="https://github.com/eskiu-lang">Eskiu</a> project</sub></p>
<p align="center">
  <a href="https://eskiu-lang.org">eskiu-lang.org</a> &nbsp;&middot;&nbsp;
  <a href="docs/api.md">API</a> &nbsp;&middot;&nbsp;
  <a href="examples/">Examples</a> &nbsp;&middot;&nbsp;
  <a href="https://github.com/eskiu-lang/eskiu">The language</a>
</p>

<p align="center">
  <a href="https://github.com/eskiu-packages/yaml/actions/workflows/ci.yml"><img src="https://github.com/eskiu-packages/yaml/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/version-0.1.1-6448d4" alt="Version 0.1.1">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"></a>
</p>

---

`yaml` reads the YAML that configuration files use into a `<json>` `JsonValue`, so a program
reads its settings with `json_get` paths and can write them back out as JSON. It is pure
Eskiu, with no library to install.

- **The YAML 1.2 core schema.** Block mappings and sequences, flow collections, plain,
  quoted and block scalars (`|`, `>`, chomping and indentation indicators), comments and
  the `---`/`...` markers. Plain scalars become null, booleans, numbers or strings as the
  YAML 1.2 core schema says (`yes` stays a string).
- **Errors with a place.** A failure gives its line, column and reason, and a duplicate
  key is an error.
- **Checked.** The expected results of the tests are compared with ruamel.yaml, and every
  prefix and one-byte change of a sample document runs under AddressSanitizer in CI.

## Reading a file

```eskiu
import <io>;
import <json>;
import <yaml>;

int main() {
    YamlError err;
    *JsonValue cfg = yaml_load("service.yaml", &err);
    if (cfg == null) {
        printf("service.yaml:%d:%d: %s\n", err.line, err.col, err.message.cstr());
        return 1;
    }
    defer JsonValue_free(cfg);
    *JsonValue port = json_get(cfg, "server.port");
    *JsonValue model = json_get(cfg, "models[0].path");
    printf("port %d, model %s\n", port != null ? (int)port.num : 80,
           model != null ? model.str.cstr() : "none");
    return 0;
}
```

[`examples/config.esk`](examples/config.esk) prints a YAML file, or one value of it, as JSON:

```
$ eskiuc run examples/config.esk -- examples/service.yaml 'models[1].scales'
[
  2.7,
  4
]
```

`yaml_parse` reads a string and `yaml_parse_bytes` a buffer.

## Documentation

- [What is left out](docs/README.md#what-is-left-out)
- [Contributing](docs/README.md#contributing)
- [API reference](docs/api.md): every public function and type

## Install

```bash
eskiuc add yaml --git https://github.com/eskiu-packages/yaml --rev v0.1.1
```

It needs Eskiu 0.14 or newer and runs everywhere Eskiu does.

## License

MIT. See [LICENSE](LICENSE).
