import unittest
from pbx_gs_python_utils.utils.Dev import Dev
from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper


class test_Deploy_Lambda_Functions(Test_Helper):

    def setUp(self):
        super().setUp()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # def test_deploy_lambda_functions(self):
    #     targets = [
    #                 'osbot_jupyter.lambdas.osbot'      ,   #   osbot.py    OSBot_Commands
    #                 #'osbot_jupyter.lambdas.screenshot'
    #                ]
    #     result = ""
    #     for target in targets:
    #         Deploy(target).deploy()
    #         result += " • {0}\n".format(target)
    #
    #     text        = ":hotsprings: [osbot-gsuite] updated lambda functions"
    #     attachments = [{'text': result, 'color': 'good'}]
    #     slack_message(text, attachments)  # gs-bot-tests
    #     Dev.pprint(text, attachments)

    # this is the main lambda (responsible for the `jupyter/jp` command
    def test_deploy_osbot_jupyter(self):
        self.result = Deploy().deploy_lambda__jupyter('osbot_jupyter.lambdas.osbot')

    def test_deploy_start_server(self):
        self.result = Deploy().deploy_lambda__jupyter('osbot_jupyter.lambdas.start_server')

    def test_deploy_screenshot(self):
        self.result = Deploy('osbot_jupyter.lambdas.screenshot').deploy_screenshot()

    def test_deploy_jupyter_web(self):
        self.result = Deploy('osbot_jupyter.lambdas.jupyter_web').deploy_jupyter_web()

if __name__ == '__main__':
    unittest.main()
