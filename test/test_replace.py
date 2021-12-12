import logging
import os

from foliant_test.preprocessor import PreprocessorTestFramework
from unittest import TestCase


def rel_name(path: str):
    return os.path.join(os.path.dirname(__file__), path)


logging.disable(logging.CRITICAL)


class TestAnchors(TestCase):
    def setUp(self):
        self.ptf = PreprocessorTestFramework('replace')

    def test_dictionary(self):
        self.ptf.options = {
            'dictionary': {
                'cats': 'dogs',
                'Cats': 'Birds',
                'hamsters': 'mice'
            }
        }
        self.ptf.test_preprocessor(
            input_mapping={
                'index.md': 'I love cats. Cats are better than hamsters!\n'
            },
            expected_mapping={
                'index.md': 'I love dogs. Birds are better than mice!\n'
            }
        )

    def test_re_dictionary(self):
        self.ptf.options = {
            're_dictionary': {
                r'\[(.+?)\]': r'(\1)',
                'love(?=:)': 'like',
            }
        }
        self.ptf.test_preprocessor(
            input_mapping={
                'index.md': 'I love: [cats], [dogs], [hamsters]. I also love mice.\n'
            },
            expected_mapping={
                'index.md': 'I like: (cats), (dogs), (hamsters). I also love mice.\n'
            }
        )

    def test_legacy(self):
        self.ptf.options = {
            'dictionary': {
                'cats': 'dogs',
                'Cats': 'Birds',
                'hamsters': 'mice',
            },
            'dictionary_filename': rel_name('dict.yml')
        }
        self.ptf.test_preprocessor(
            input_mapping={
                'index.md': 'I love cats. Cats are better than hamsters!\n'
            },
            expected_mapping={
                'index.md': 'I like dogs. Birds are better than mice!\n'
            }
        )
