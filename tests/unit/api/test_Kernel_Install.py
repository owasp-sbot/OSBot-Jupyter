import textwrap
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Kernel_Install import Kernel_Install, Kernel_Install_Inside_Jupyter
from osbot_jupyter.helpers.Test_Server import Test_Server
from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel

class test_Kernel_Install_Inside_Jupyter(TestCase):

    def setUp(self):
        self.kernel_class   = Echo_Kernel
        self.kernel_install = Kernel_Install_Inside_Jupyter(self.kernel_class)
        self.result         = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test__init__(self):
        assert self.kernel_install.kernel_name   == 'Echo'
        assert self.kernel_install.kernel_module == 'osbot_jupyter.kernels.Echo_Kernel'
        assert self.kernel_install.kernel_spec.get('language')  == 'text'

class test_Kernel_Install(TestCase):

    def setUp(self):
        self.delete_on_exit = True
        self.kernel_class   = Echo_Kernel
        self.kernel_name    = Echo_Kernel().kernel_name
        self.python_kernel  = Test_Server().docker().jupyter_kernel().new()
        self.kernel_install = Kernel_Install(self.kernel_name, self.kernel_class, self.python_kernel)
        self.result         = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)
        if self.delete_on_exit:
            self.python_kernel.delete()

    def test__init__(self):
        assert self.kernel_install.kernel_name   == 'Echo'
        assert self.kernel_install.kernel_class  == 'Echo_Kernel'
        assert self.kernel_install.kernel_module == 'osbot_jupyter.kernels.Echo_Kernel'

    def test_current_kernels(self):
        assert len(set(self.kernel_install.current_kernels())) > 0

    def test_install(self):
        assert self.kernel_install.install().get('status') == 'ok'
        assert self.kernel_name.lower() in set(self.kernel_install.current_kernels())

        assert self.kernel_install.uninstall().get('status') == 'ok'
        assert self.kernel_name.lower() not in self.kernel_install.current_kernels().keys()