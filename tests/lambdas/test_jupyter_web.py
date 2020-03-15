import base64
from unittest                           import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from pbx_gs_python_utils.utils.Dev      import Dev
from osbot_aws.helpers.Lambda_Package   import Lambda_Package

from osbot_jupyter.lambdas.jupyter_web import run


class test_jupyter_web(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_jupyter.lambdas.jupyter_web'
        self.short_id    = 'd18e2'                               # todo: get this from
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None
        self.png_data    = None

        #Deploy(self.lambda_name).deploy_jupyter_web()  # when wanting to deploy it                                    # use when wanting to update lambda function
    def test_update_lambda_function(self):
        Deploy().deploy_lambda__jupyter_web('osbot_jupyter.lambdas.jupyter_web')

    def test_invoke_directly____preview(self):
        event = {"params": ['preview',self.short_id,'asd', {}]}
        self.png_data = run(event, {})[0]

    def test_invoke_directly____screenshot(self):
        event = {"params": ['screenshot', self.short_id,{}]}
        self.result = run(event, {})[0]
        #self.png_data = run(event, {})[0]

    def test_screenshot(self):
        #self.test_update_lambda_function()
        url = '/upwork-jupyter/how-tos/get-list-of-jira-issues-created-recently.ipynb' #'/abc'
        payload       = { "params": ['screenshot', self.short_id, url, {}]}
        self.result   = self.aws_lambda.invoke(payload)
        #self.png_data =  self.aws_lambda.invoke(payload)[0]
        #self.png_data =  self.aws_lambda.invoke(payload)[0]


    def test_preview__404(self):
        #self.test_update_lambda_function()
        url = '/abc'
        payload       = { "params": ['preview', self.short_id, url, {}]}
        #self.result   = self.aws_lambda.invoke(payload)
        self.png_data =  self.aws_lambda.invoke(payload)[0]

    def test_bug__preview__notebook_that_is_raising_exception(self):
        build_id = CodeBuild_Jupyter_Helper().get_active_build_id(project_name='OSBot-Jupyter')
        url = 'upwork-jupyter/reports/issues-created-in-last-24h.ipynb?show-code'
        payload       = { "params": ['preview', build_id, url, {}]}

        # invoke direclty
        self.png_data = run(payload, {})[0]

        # invoke lambda
        self.test_update_lambda_function()
        self.result = self.aws_lambda.invoke(payload)
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





