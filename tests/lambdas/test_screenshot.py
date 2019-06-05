import base64
from unittest                           import TestCase

from osbot_aws.Globals import Globals
from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

from osbot_jupyter.Deploy import Deploy


class test_run_command(TestCase):
    def setUp(self):

        Deploy('osbot_jupyter.lambdas.screenshot')\
            #.deploy_lambda__screenshot()
        self.short_id   = '3e27b'
        self.aws_lambda = Lambda('osbot_jupyter.lambdas.screenshot')
        self.result = None
        self.png_data = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_screenshot(self):
        payload     = { 'short_id' : self.short_id, 'path':'', 'width':800}
        self.png_data = self.aws_lambda.invoke(payload)
        #self.result =  self.aws_lambda.invoke(payload)

    def test_screenshot__google(self):
        payload     = { 'short_id' : self.short_id, 'path':'https://www.google.com', 'width':800}
        #self.png_data = self.aws_lambda.invoke(payload)
        self.result =  self.aws_lambda.invoke(payload)

    def test_screenshot___with_url(self):
        notebook = 'https://442174ec.ngrok.io/nbconvert/html/users/Lauren/my-first-wardley-map.ipynb?download=false'
        payload = {'short_id': self.short_id, 'path': notebook, 'width': 2000, 'height': 12000}
        self.png_data = self.aws_lambda.invoke(payload)





