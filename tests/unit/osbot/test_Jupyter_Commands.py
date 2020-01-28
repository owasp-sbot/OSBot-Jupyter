from unittest import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from osbot_jupyter.osbot.Jupyter_Commands import Jupyter_Commands


class test_Jupyter_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.jp_commands = Jupyter_Commands()
        self.result = None
        #self.team_id   = 'T7F3AUXGV'
        self.channel   = 'DRE51D4EM'
        self.short_id = '42117'

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

    # def test_get_active_builds(self):
    #     self.result = self.jp_commands.get_active_builds()
    #
    # def test_get_active_server(self):
    #     self.result = self.jp_commands.get_active_server()

    def test_start(self):
        # repo = 'gs-notebook-risks'
        # repo = 'gs-notebook-detect'

        repo_name = 'gs-notebook-gscs'
        self.result = self.jp_commands.start(params=[repo_name], channel=self.channel)

    def test_version(self):
        self.result = self.jp_commands.version()


    # via Lambda

    def test_update_lambda(self):
        self.result = Deploy().deploy_lambda__jupyter('osbot_jupyter.lambdas.osbot')
        #Deploy('osbot_jupyter.lambdas.osbot').deploy()

    def invoke_lambda(self,params):
        aws_lambda = Lambda('osbot_jupyter.lambdas.osbot')
        payload = {'params': params}
        return aws_lambda.invoke(payload)

    def test_web__via_lambda(self):
        self.test_update_lambda()
        self.result = self.invoke_lambda(['web'])

    def test_version__via_lambda(self):
        self.result = self.invoke_lambda(['version'])