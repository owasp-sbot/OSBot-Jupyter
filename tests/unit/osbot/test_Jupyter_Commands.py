from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.osbot.Jupyter_Commands import Jupyter_Commands


class test_Jupyter_Commands(TestCase):

    def setUp(self):
        self.jp_commands = Jupyter_Commands()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_get_active_builds(self):
        self.result = self.jp_commands.get_active_builds()

    def test_abc(self):
        import osbot_jupyter.kernels
        self.result = dir(osbot_jupyter)