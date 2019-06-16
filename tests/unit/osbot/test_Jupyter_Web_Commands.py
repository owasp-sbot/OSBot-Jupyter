import base64
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.Deploy import Deploy
from osbot_jupyter.osbot.Jupyter_Web_Commands import Jupyter_Web_Commands


class test_Jupyter_Web_Commands(TestCase):

    def setUp(self):
        self.short_id    = '12d62'
        self.result      = None
        self.png_data    = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_screenshot(self):
        params = [self.short_id]
        self.png_data = Jupyter_Web_Commands.screenshot(params=params)

    def test_create_file__notebook(self):
        notebook_path = 'users/gsbot/aaa.ipynb'
        first_cell    = '40 +2'
        params = [self.short_id,notebook_path, first_cell]
        self.result = Jupyter_Web_Commands.create_file(params=params)

    def test_create_file__txt(self):
        notebook_path = 'users/gsbot/aaa.txt'
        first_cell    = 'this is some text content.'
        params = [self.short_id,notebook_path, first_cell]
        self.result = Jupyter_Web_Commands.create_file(params=params)


    def test_execute_python(self):
        tmp_value = Misc.random_string_and_numbers()
        code      = "tmp_var='{0}' \nprint(tmp_var)".format(tmp_value)
        params = [self.short_id, code, { 'original':'slack data'}]
        self.result = Jupyter_Web_Commands.execute_python(params=params)
        #self.png_data = Jupyter_Web_Commands.execute_python(params=params)

    def test_execute_python__via_lambda(self):
        self.result = Deploy('osbot_jupyter.lambdas.jupyter_web').deploy_jupyter_web()

        payload = {'params':['execute_python', self.short_id, '20*2 + 2', {}] , 'channel': 'DG30MH0KV', 'team_id' : 'T0SDK1RA8' }
        self.result = Lambda('osbot_jupyter.lambdas.jupyter_web').invoke(payload)

    # deploy lambda

    def test_deploy_jupyter_web(self):
        self.result = Deploy('osbot_jupyter.lambdas.jupyter_web').deploy_jupyter_web()
