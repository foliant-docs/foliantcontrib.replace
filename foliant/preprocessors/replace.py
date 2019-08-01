'''
Preprocessor for Foliant documentation authoring tool.
Replaces text by dictionary.
'''


import re
from pathlib import Path
from yaml import load, Loader

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'dictionary_filename': 'replace_dictionary.yml',
        'with_confirmation': False,
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('maketablesmultiline')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._dictionary_filename = self.options['dictionary_filename']
        self._with_confirmation = self.options['with_confirmation']


    def apply(self):
        self.logger.info('Applying preprocessor')

        with open(self._dictionary_filename, encoding='utf8') as dict_file:
            replace_dictionary = load(dict_file, Loader)

        for markdown_file_path in self.working_dir.rglob('*.md'):
            self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

            with open(markdown_file_path, encoding='utf8') as file_to_read:
                file_data = list(file_to_read)

            for i, string in enumerate(file_data):
                if 'words' in replace_dictionary:
                    for word in replace_dictionary['words']:
                        if word in string and not '![' in string:
                            if self._with_confirmation:
                                new_string = string.replace(word, replace_dictionary['words'][word])
                                user_answer = ''
                                while user_answer not in ('y','n'):
                                    user_answer = input(f'\nReplace\n"{string.strip()}" with\n"{new_string.strip()}"?\nEnter y or n:')
                                    if user_answer == 'y':
                                        string = new_string
                                        file_data[i] = new_string
                            else:
                                string = string.replace(word, replace_dictionary['words'][word])
                                file_data[i] = string
                if 'regexs' in replace_dictionary:
                    for regex in replace_dictionary['regexs']:
                        if re.search(regex, string) and not '![' in string:
                            if self._with_confirmation:
                                if 'lambda' in replace_dictionary['regexs'][regex]:
                                    new_string = re.sub(regex, eval(replace_dictionary['regexs'][regex]), string)
                                else:
                                    new_string = re.sub(regex, replace_dictionary['regexs'][regex], string)
                                user_answer = ''
                                while user_answer not in ('y','n'):
                                    user_answer = input(f'\nReplace\n"{string.strip()}" with\n"{new_string.strip()}"?\nEnter y or n:')
                                    if user_answer == 'y':
                                        string = new_string
                                        file_data[i] = new_string
                            else:
                                if 'lambda' in replace_dictionary['regexs'][regex]:
                                    string = re.sub(regex, eval(replace_dictionary['regexs'][regex]), string)
                                else:
                                    string = re.sub(regex, replace_dictionary['regexs'][regex], string)
                                file_data[i] = string

            with open(markdown_file_path, 'w', encoding="utf-8") as file_to_write:
                for string in file_data:
                    file_to_write.write(string)

        self.logger.info('Preprocessor applied')
