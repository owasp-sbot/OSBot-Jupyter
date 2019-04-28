from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.helpers.GSBot_Execution import GSBot_Execution


class test_GSBot_Execution(TestCase):

    def setUp(self):
        self.gsbot  = GSBot_Execution()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_invoke(self):
        message = 'hello...'
        Dev.pprint(self.gsbot.invoke(message))

