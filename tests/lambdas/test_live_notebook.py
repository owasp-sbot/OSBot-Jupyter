import base64
from unittest                           import TestCase
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

class test_run_command(TestCase):
    def setUp(self):
        self.short_id   = '0957b'
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.live_notebook')
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
        payload     = { 'short_id' : self.short_id, 'path':'examples/simple-commands', 'width':800}
        self.png_data = self.aws_lambda.invoke(payload)
        #self.result =  self.aws_lambda.invoke(payload)

