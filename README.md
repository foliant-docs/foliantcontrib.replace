[![](https://img.shields.io/pypi/v/foliantcontrib.replace.svg)](https://pypi.org/project/foliantcontrib.replace/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.replace.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.replace)

# Replace text for Foliant

Preprocessor for simple search and replace in Markdown sources with support of regular expressions.


## Installation

```shell
$ pip install foliantcontrib.replace
```

## Config

To enable the preprocessor, add `replace` to `preprocessors` section in the project config:

```yaml
preprocessors:
  - replace
```

The preprocessor has two options:

```yaml
preprocessors:
  - replace:
      dictionary:
        Mike: Michael
        Sam: Samuel
        Tim: Timoel
      re_dictionary:
        '!\[\]\((.+?)\)': '![Figure](\1)'

```

`dictionary`
:   YAML mapping where key is string to replace, value is the replacement string.

`re_dictionary`
:   YAML mapping where key is [Python regular expression](https://docs.python.org/3/howto/regex.html) pattern, value is the replacement string.

## Usage

Fill up the `dictionary` or/and `re_dictionary` in preprocessor options and the keys will be replaced with values.

For example, if you wish that all images without title in your Markdown sources were titled "Figure", use the following config:

```yaml
preprocessors:
  - replace:
      re_dictionary:
        '!\[\]\((.+?)\)': '![Figure](\1)'

```

You can also apply a sequence of regex substitions. Like case-insensitive link insertion as shown in the example below:

```yaml
preprocessors:
  - replace:
      re_dictionary:
        '`(?i)(wikipedia)`': '[\1](https://www.wikipedia.org/)'
        '`(?i)(github)`': '[\1](https://github.com/)'
```
