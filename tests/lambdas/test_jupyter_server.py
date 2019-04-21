from unittest                           import TestCase
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package
from osbot_jupyter.api.Jupyter          import Jupyter

class test_run_command(TestCase):
    def setUp(self):
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.jupyter_server')
        self.result     = None

        self.aws_lambda.update_code()       # use when wanting to update lambda function

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test_invoke_lambda(self):
        payload     = { }
        self.result = self.aws_lambda.invoke(payload)


    # def test_ping(self):
    #     payload     = { 'task_name': 'ping'}
    #     self.result = self.aws_lambda.invoke(payload)


