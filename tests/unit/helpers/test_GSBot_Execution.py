from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jupyter.helpers.GSBot_Execution import GSBot_Execution


class test_GSBot_Execution(TestCase):

    def setUp(self):
        self.gsbot  = GSBot_Execution()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_invoke(self):
        message = 'help'
        (text,attachments) = self.gsbot.invoke(message)
        Dev.pprint(text,attachments)

    def test_invoke_jira__version(self):
        message = 'jira version'
        text = self.gsbot.invoke(message)
        Dev.pprint(text)

    def test_invoke_jira__links(self):
        message = 'jira links RISK-12 all 1'
        text = self.gsbot.invoke(message)
        Dev.pprint(text)

