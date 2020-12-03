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
                new_string = string
                if 'words' in replace_dictionary:
                    for word in replace_dictionary['words']:
                        check_again = True
                        while check_again:
                            if word in new_string:
                                if '](' in new_string:
                                    text_part = new_string.split('[')[1].split('](')[0]
                                    new_string = re.sub('(.*\[)(.*)(]\(.*)', '\g<1>' + text_part.replace(word, replace_dictionary['words'][word]) + '\g<3>', new_string)
                                else:
                                    new_string = new_string.replace(word, replace_dictionary['words'][word])
                                if self._with_confirmation:
                                    user_answer = ''
                                    while user_answer not in ('y','n'):
                                        user_answer = input(f'\nReplace\n"{new_string.strip()}" with\n"{new_string.strip()}"?\nEnter y or n:')
                                        if user_answer == 'y':
                                            file_data[i] = new_string
                                else:
                                    file_data[i] = new_string
                            else:
                                check_again = False
                if 'regexs' in replace_dictionary:
                    for regex in replace_dictionary['regexs']:
                        if re.search(regex, new_string):
                            if 'lambda' in replace_dictionary['regexs'][regex]:
                                if '](' in string:
                                    text_part = new_string.split('[')[1].split('](')[0]
                                    new_string = re.sub('(.*\[)(.*)(]\(.*)', '\g<1>' + re.sub(regex, eval(replace_dictionary['regexs'][regex]), text_part) + '\g<3>', new_string)
                                else:
                                    new_string = re.sub(regex, eval(replace_dictionary['regexs'][regex]), new_string)
                            else:
                                if '](' in new_string:
                                    text_part = new_string.split('[')[1].split('](')[0]
                                    new_string = re.sub('(.*\[)(.*)(]\(.*)', '\g<1>' + re.sub(regex, replace_dictionary['regexs'][regex], text_part) + '\g<3>', new_string)
                                else:
                                    new_string = re.sub(regex, replace_dictionary['regexs'][regex], new_string)
                            if self._with_confirmation:
                                user_answer = ''
                                while user_answer not in ('y','n'):
                                    user_answer = input(f'\nReplace\n"{new_string.strip()}" with\n"{new_string.strip()}"?\nEnter y or n:')
                                    if user_answer == 'y':
                                        file_data[i] = new_string
                            else:
                                file_data[i] = new_string

            with open(markdown_file_path, 'w', encoding="utf-8") as file_to_write:
                for string in file_data:
                    file_to_write.write(string)

        self.logger.info('Preprocessor applied')
