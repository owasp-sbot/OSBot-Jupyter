import base64
from unittest                           import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils.Dev import Dev


class test_run_command(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_jupyter.lambdas.screenshot'
        self.short_id   = 'ec6a1'
        self.aws_lambda = Lambda(self.lambda_name)
        #Deploy(self.lambda_name).deploy_screenshot()                                    # use when wanting to update lambda function
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

    def test_update_lambda(self):
        lambda_name = 'osbot_jupyter.lambdas.screenshot'
        Deploy().deploy_lambda__jupyter_web(lambda_name)

    def test_screenshot(self):
        self.test_update_lambda()
        payload     = { 'short_id' : self.short_id, 'path':'', 'width':800}
        self.png_data = self.aws_lambda.invoke(payload)
        #self.result =  self.aws_lambda.invoke(payload)

    def test_screenshot__google(self):
        payload     = { 'short_id' : self.short_id, 'path':'https://www.google.com', 'width':800}
        self.png_data = self.aws_lambda.invoke(payload)
        #self.result =  self.aws_lambda.invoke(payload)

    def test_screenshot___with_url(self):
        notebook = 'https://fcd32272.ngrok.io/nbconvert/html/users/dinis/rdf/part-1-loading-the-rdf-file.ipynb?download=false'
        payload = {'short_id': self.short_id, 'path': notebook, 'width': 2000, 'height': 12000}
        self.png_data = self.aws_lambda.invoke(payload)

    def test_screenshot___with_delay(self):
        short_id = '05e'
        #notebook = 'https://687f4814.ngrok.io/notebooks/users/dinis/simple-tests.ipynb'
        notebook = 'https://687f4814.ngrok.io/nbconvert/html/users/dinis/simple-tests.ipynb?download=false&osbot-no-code'
        payload = {
                    'short_id': short_id,
                    'path'    : notebook,
                    'width'   : 1500    ,
                    'height'  : 200     ,
                    'delay'   : 0       }
        self.png_data = self.aws_lambda.invoke(payload)





