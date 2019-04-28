from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Kernel_Install import Kernel_Install


class test_Kernel_Install(TestCase):

    def setUp(self):
        self.kernel_name    = 'Echo'
        self.kernel_install = Kernel_Install(self.kernel_name)
        self.result         = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test__init__(self):
        self.result = self.kernel_install.kernel_name