import base64
from unittest                           import TestCase
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package
from osbot_jupyter.api.Jupyter          import Jupyter

class test_run_command(TestCase):
    def setUp(self):
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.browser')
        self.result     = None
        self.png_data   = None
        self.aws_lambda.add_module('osbot_browser')
        self.aws_lambda.update_code()       # use when wanting to update lambda function

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_invoke_lambda(self):
        payload     = { 'url' : 'https://www.google.com/abc'}
        self.png_data = self.aws_lambda.invoke(payload)

