import base64
from unittest                           import TestCase

from osbot_aws.Globals import Globals
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

from osbot_jupyter.lambdas.osbot import run


class test_run_command(TestCase):
    def setUp(self):
        self.bot_name = 'oss_bot'
        self.profile_name = 'gs-detect-aws'  # 654386450934
        self.region_name = 'eu-west-2'

        Globals.aws_session_profile_name = self.profile_name
        Globals.aws_session_region_name = self.region_name
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.osbot')
        self.result     = None
        #self.aws_lambda.update_code()       # use when wanting to update lambda function

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)


    def test_invoke_directly(self):
        payload = {'params': ['aaaa']}
        self.result = run(payload,{})

    # def test_invoke_directly__get_active_server(self):
    #     payload = {'params': ['get_active_server']}
    #     self.result = run(payload,{})


    def test_invoke_lambda(self):
        payload     = { 'data' : { 'params': ['help']}}
        self.result = self.aws_lambda.invoke(payload)


    # def test_invoke_get_active_server(self):
    #     payload     = { 'params': ['get_active_server']}
    #     self.result = self.aws_lambda.invoke(payload)

    def test_invoke_start_server(self):
        payload     = { 'params': ['start_server']}
        self.result = self.aws_lambda.invoke(payload)

    def test_invoke_servers(self):
        self.aws_lambda.update_code()
        payload     = {  'params': ['servers'], 'data': {'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV'}}
        self.result = self.aws_lambda.invoke(payload)

    def test___update_lambda_function(self):
        self.aws_lambda.update_code()  # use when wanting to update lambda function
