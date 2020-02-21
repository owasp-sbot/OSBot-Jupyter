import base64
from unittest                           import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_jupyter.lambdas.osbot import run


class test_run_command(Test_Helper):
    def setUp(self):
        super().setUp()
        self.aws_lambda = Lambda('osbot_jupyter.lambdas.osbot')
        self.result     = None
        #self.aws_lambda.update_code()       # use when wanting to update lambda function

    def test_update_lambda(self):
        Deploy().deploy_lambda__jupyter_web('osbot_jupyter.lambdas.osbot')

    def test_invoke_directly(self):
        payload = {'params': ['aaaa']}
        self.result = run(payload,{})

    def test_invoke_directly__get_active_server(self):
        payload = {'params': ['get_active_server']}
        self.result = run(payload,{})


    def test_invoke_lambda__version(self):
        payload     = { 'params': ['version']}
        self.result = self.aws_lambda.invoke(payload)


    # def test_invoke_get_active_server(self):
    #     payload     = { 'params': ['get_active_server']}
    #     self.result = self.aws_lambda.invoke(payload)

    # def test_invoke_start_server(self):
    #     payload     = { 'params': ['start_server']}
    #     self.result = self.aws_lambda.invoke(payload)

    # def test_invoke_servers(self):
    #     self.aws_lambda.update_code()
    #     payload     = {  'params': ['servers'], 'data': {'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV'}}
    #     self.result = self.aws_lambda.invoke(payload)

    #def test___update_lambda_function(self):
    #    self.aws_lambda.update_code()  # use when wanting to update lambda function
