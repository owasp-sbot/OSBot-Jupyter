from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Live_Notebook import Live_Notebook


class test_Live_Notebook(TestCase):

    def setUp(self):
        self.notebook = Live_Notebook(headless=False)
        self.result   = None
        self.short_id = 'dc10d'

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_set_build_from_short_id(self):
        assert self.notebook.set_build_from_short_id(self.short_id) is True
        assert self.notebook.set_build_from_short_id('aaaa'       ) is False

    def test_stop(self):
        short_id = '53dc2'
        self.result = self.notebook.set_build_from_short_id(short_id).stop()

    # api methods

    def test_screenshot(self):
        self.notebook.set_build_from_short_id(self.short_id)
        self.result = self.notebook.screenshot('examples/simple-commands',800)

