import base64
from unittest                           import TestCase

from osbot_aws.Globals import Globals
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

from osbot_jupyter.Deploy import Deploy


class test_run_command(TestCase):
    def setUp(self):

        self.aws_lambda = Lambda('osbot_jupyter.lambdas.start_server')
        self.result     = None
        self.png_data   = None

        Deploy('osbot_jupyter.lambdas.start_server').deploy()

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    # def test_invoke_lambda(self):w
    #     #payload     = { 'repo_name': 'gs-notebook-gscs',  "channel": "GDL2EC3EE", "team_id": "T7F3AUXGV"}
    #     payload     = { 'repo_name': 'gs-notebook-risks', 'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV', 'user': 'U7ESE1XS7'}
    #     self.result = self.aws_lambda.invoke(payload)

    def test_invoke_lambda_bad_repo(self):
        payload     = { 'repo_name': 'gs-notebook-AAAAA', "team_id" : "T7F3AUXGV", "channel": "GDL2EC3EE"}
        self.result = self.aws_lambda.invoke(payload)


    def test_invoke_async(self):
        payload = {'repo_name': 'gs-notebook-risks', 'channel': 'GDL2EC3EE', 'team_id': 'T7F3AUXGV', 'user': 'U7ESE1XS7'}
        result = Lambda('osbot_jupyter.lambdas.start_server').invoke_async(payload)
        self.result = result


    def test_start_server_directly(self):
        repo = 'jp-tests'
        from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
        self.result = CodeBuild_Jupyter_Helper().start_build_for_repo(repo)