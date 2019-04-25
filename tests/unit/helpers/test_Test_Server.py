from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Test_Server(TestCase):

    def setUp(self):
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_stop_build(self):
        from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter_Helper
        code_build_helper = CodeBuild_Jupyter_Helper()
        self.result = code_build_helper.stop_all_active()

    def test_codebuild(self):
        test_server = Test_Server().codebuild()
        self.result =  test_server.url()
