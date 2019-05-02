from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api_notebook.Jp_GSheets import Jp_GSheets


class test_Jp_GSheets(TestCase):

    def setUp(self):
        self.file_id    = '1_Bwz6z34wALFGb1ILUXG8CtF1-Km6F9_sGXnAu4gewY'
        self.sheet_name = 'Jira Data'
        self.sheets     = Jp_GSheets(self.file_id, self.sheet_name)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_metadata(self):
        self.result = self.sheets.metadata()

    def test_link(self):
        self.result = self.sheets.link()




