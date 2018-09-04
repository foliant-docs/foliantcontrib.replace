'''
Preprocessor for Foliant documentation authoring tool.
Makes markdown tables multiline before pandoc processing.
'''


import re
from pathlib import Path
from yaml import load

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'dictionary_filename': 'replace_dictionary.yml',
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('maketablesmultiline')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._dictionary_filename = self.options['dictionary_filename']


    def apply(self):
        self.logger.info('Applying preprocessor')

        with open(self._dictionary_filename, encoding='utf8') as dict_file:
            replace_dictionary = load(dict_file)

        for markdown_file_path in self.working_dir.rglob('*.md'):
            self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

            with open(markdown_file_path, encoding='utf8') as file_to_read:
                file_data = list(file_to_read)

            for i, string in enumerate(file_data):
                if 'words' in replace_dictionary:
                    for word in replace_dictionary['words']:
                        if word in string:
                            file_data[i] = string.replace(word, replace_dictionary['words'][word])
                if 'regexs' in replace_dictionary:
                    for regex in replace_dictionary['regexs']:
                        if re.search(regex, string):
                            file_data[i] = re.sub(regex, replace_dictionary['regexs'][regex], string)

            with open(markdown_file_path, 'w', encoding="utf-8") as file_to_write:
                for string in file_data:
                    file_to_write.write(string)

        self.logger.info('Preprocessor applied')
