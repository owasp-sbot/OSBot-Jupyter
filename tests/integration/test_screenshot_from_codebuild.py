from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Jupyter import Jupyter


class test_screenshot_from_codebuild(TestCase):
    def setUp(self):
        self.jp = Jupyter()

    def test_here(self):
        Dev.pprint('42')

