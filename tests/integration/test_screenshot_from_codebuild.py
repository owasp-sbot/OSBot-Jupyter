import base64
from unittest import TestCase

from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_utils.utils.Dev import Dev

from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter


class test_screenshot_from_codebuild(TestCase):
    def setUp(self):
        self.code_build = CodeBuild_Jupyter()
        self.jp         = Jupyter()
        self.png_data   = None

    def tearDown(self):
        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_get_screenshot_using_local_chrome(self):
        url, token = self.code_build.get_server_details_from_logs()
        self.jp.set_url(url).set_token(token)
        self.jp.login()
        #self.jp.open('aaa')
        self.png_file = self.jp.screenshot()
        Dev.pprint(self.png_file)

    def test_get_screenshot_using_lambda(self):
        self.aws_lambda = Lambda_Package('osbot_jupyter.lambdas.jupyter_server')
        url, token = self.code_build.get_server_details_from_logs()
        #print(url,token)
        #return
        notebook = 'test-1'
        payload = {'url': url, 'token': token, 'notebook': notebook}
        self.png_data = self.aws_lambda.invoke(payload)

