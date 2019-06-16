import base64
from unittest                           import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

from osbot_jupyter.Deploy import Deploy
from osbot_jupyter.lambdas.jupyter_web import run


class test_run_command(TestCase):

    def setUp(self):
        self.lambda_name = 'osbot_jupyter.lambdas.jupyter_web'
        self.short_id    = '42117'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None
        self.png_data    = None

        Deploy(self.lambda_name).deploy_jupyter_web()  # when wanting to deploy it                                    # use when wanting to update lambda function


    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_invoke_directly____screenshot(self):
        event = {"params": ['screenshot', '42117aa']}
        self.result = run(event, {})

    def test_screenshot(self):
        payload     = { "params": ['screenshot', '42117']}
        self.result =  self.aws_lambda.invoke(payload)
        #self.png_data =  self.aws_lambda.invoke(payload)[0]

    # def test_screenshot__google(self):
    #     payload     = { 'short_id' : self.short_id, 'path':'https://www.google.com', 'width':800}
    #     self.png_data = self.aws_lambda.invoke(payload)
    #     #self.result =  self.aws_lambda.invoke(payload)
    #
    # def test_screenshot___with_url(self):
    #     notebook = 'https://fcd32272.ngrok.io/nbconvert/html/users/dinis/rdf/part-1-loading-the-rdf-file.ipynb?download=false'
    #     payload = {'short_id': self.short_id, 'path': notebook, 'width': 2000, 'height': 12000}
    #     self.png_data = self.aws_lambda.invoke(payload)
    #
    # def test_screenshot___with_delay(self):
    #     short_id = '05e'
    #     #notebook = 'https://687f4814.ngrok.io/notebooks/users/dinis/simple-tests.ipynb'
    #     notebook = 'https://687f4814.ngrok.io/nbconvert/html/users/dinis/simple-tests.ipynb?download=false&osbot-no-code'
    #     payload = {
    #                 'short_id': short_id,
    #                 'path'    : notebook,
    #                 'width'   : 1500    ,
    #                 'height'  : 200     ,
    #                 'delay'   : 0       }
    #     self.png_data = self.aws_lambda.invoke(payload)





