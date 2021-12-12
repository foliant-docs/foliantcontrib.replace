'''
Preprocessor for Foliant documentation authoring tool.
Replaces text by dictionary.
'''
import re
import yaml

from foliant.preprocessors.utils.preprocessor_ext import BasePreprocessorExt


class Preprocessor(BasePreprocessorExt):
    defaults = {
        'dictionary': {},
        're_dictionary': {},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('replace')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._dictionary = {}
        self._re_dictionary = {}

        self.load_legacy()

        self._dictionary.update(self.options['dictionary'])
        self._re_dictionary.update(
            {re.compile(k): v for k, v in self.options['re_dictionary'].items()}
        )

    def load_legacy(self):
        if 'dictionary_filename' in self.options:
            self.logger.debug('Legacy parameter detected, adding to dictionary')
            with open(self.options['dictionary_filename']) as f:
                dict = yaml.load(f, yaml.Loader)
            if 'words' in dict:
                self._dictionary.update(dict['words'])
            if 'regexs' in dict:
                self._re_dictionary.update(
                    {re.compile(k): v for k, v in dict['regexs'].items()}
                )

    def _process_file(self, content):
        processed = content
        for pattern, replacement in self._dictionary.items():
            self.logger.debug(f'replacing {pattern=} with {replacement=}')
            processed = processed.replace(pattern, replacement)
        for pattern, replacement in self._re_dictionary.items():
            self.logger.debug(f'replacing {pattern=} with {replacement=}')
            processed = pattern.sub(replacement, processed)
        return processed

    def apply(self):
        self._process_all_files(func=self._process_file, buffer=False)
        self.logger.info('Preprocessor applied')
