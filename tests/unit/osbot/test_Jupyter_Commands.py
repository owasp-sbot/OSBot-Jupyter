from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.osbot.Jupyter_Commands import Jupyter_Commands


class test_Jupyter_Commands(TestCase):

    def setUp(self):
        self.jp_commands = Jupyter_Commands()
        self.result = None
        self.team_id   = 'T7F3AUXGV'
        self.channel   = 'GDL2EC3EE'
        self.short_id = '0957b'

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_contents(self):
        path = 'scenarios'
        self.result = self.jp_commands.contents(params=[self.short_id, path, {}], team_id=self.team_id, channel=self.channel)

    def test_screenshot(self):
        params = ['dc10d', 'examples/simple-commands',1200]
        self.result = self.jp_commands.screenshot(params=params, team_id=self.team_id, channel=self.channel)

    def test_servers(self):
        self.result = self.jp_commands.servers()

    def test_get_active_builds(self):
        self.result = self.jp_commands.get_active_builds()

    def test_get_active_server(self):
        self.result = self.jp_commands.get_active_server()

    def test_start_build(self):
        # repo = 'gs-notebook-risks'
        # repo = 'gs-notebook-detect'
        print()
        repo_name = 'gs-notebook-gscs'
        self.result = self.jp_commands.start_server(params=[repo_name], team_id=self.team_id, channel=self.channel)