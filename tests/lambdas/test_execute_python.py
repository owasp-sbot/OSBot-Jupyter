import base64
from unittest                           import TestCase
from osbot_utils.utils.Dev import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

class test_run_command(TestCase):
    def setUp(self):
        self.short_id   = '3ddc8'
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.execute_python')
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

    def test_execute_python(self):
        code          = '40+3'
        target        = None
        keep_contents = None
        payload  = { 'short_id' : self.short_id, 'python_code':code, target:target, keep_contents:keep_contents }
        #self.png_data = self.aws_lambda.invoke(payload)
        self.result =  self.aws_lambda.invoke(payload)
        #self.png_data =  self.aws_lambda.invoke(payload)







