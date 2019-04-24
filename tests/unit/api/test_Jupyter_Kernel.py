from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Jupyter_Kernel import Jupyter_Kernel
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_Kernel(TestCase):

    def setUp(self):
        self.jp_kernel  = Test_Server().docker().jupyter_kernel()
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_list(self):
        self.result = self.jp_kernel.list()

