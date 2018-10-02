# Replace text for Foliant

Replace preprocessor reads the dictionary (yaml format) placed in foliant project folder and changes one word to another in created document.


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

The preprocessor has only one option:

```yaml
preprocessors:
  - multilinetables:
      dictionary_filename: replace_dictionary.yml
```

`dictionary_filename`
:   File in foliant project folder with dictionary in it (*replace_dictionary.yml* by default).

### Dictionary format

Dictionary stores data in yaml format. It has two sections — with words and with regular expressions. For example:

```yaml
words:
  cod: CoD
  epg: EPG
  vod: VoD
regexs:
  '!\w*!': ''
```


## Usage

Just add the preprocessor to the project config, set the dictionary and enjoy the result.
