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

    def test_get_servers(self):
        self.result = self.jp_commands.servers()

    def test_get_active_builds(self):
        self.result = self.jp_commands.get_active_builds()

    def test_start_build(self):
        # repo = 'gs-notebook-risks'
        # repo = 'gs-notebook-detect'
        print()
        team_id   = 'T7F3AUXGV'
        channel   = 'GDL2EC3EE'
        repo_name = 'gs-notebook-gscs'
        self.result = self.jp_commands.start_server(params=[repo_name], team_id=team_id, channel=channel)