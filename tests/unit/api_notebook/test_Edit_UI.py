from unittest import TestCase

from dotenv import load_dotenv

from osbot_jupyter.api_notebook.Edit_UI_Issues import Edit_UI_Issues
from osbot_utils.utils.Dev import Dev, pprint



class test_Edit_UI_Issues(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        from osbot_aws.helpers import Lambda_Helpers            # todo: add better support for this config (which should not be done here)
        Lambda_Helpers.LOG_TO_ELK_ENABLED = False
        load_dotenv()

    def setUp(self):
        self.edit_ui_issues = Edit_UI_Issues()
        self.result = None
        self.test_issue_id = 'PROJ-4'                   # todo, find solution to have test issues

    def tearDown(self):
        if self.result is not None:
            pprint(self.result)

    #def test_ctor(self):
    #    pprint(self.edit_ui_issues)

    def test_issue(self):
        issue = self.edit_ui_issues.issue(self.test_issue_id)
        assert len(set(issue)) > 0

    def test_issues(self):
        issues = self.edit_ui_issues.issues(self.test_issue_id)
        self.result = issues

    def test_summary(self):
        summary = self.edit_ui_issues.summary(self.test_issue_id)
        assert type(summary) is str
        #assert len(set(issue)) > 0