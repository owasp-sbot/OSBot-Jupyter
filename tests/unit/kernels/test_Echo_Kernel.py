from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Kernel_Install import Kernel_Install
from osbot_jupyter.helpers.Test_Server import Test_Server
from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel, Echo_Kernel_Install


class test_Echo_Kernel__Install(TestCase):

    def setUp(self):
        self.kernel_name  = "Echo"
        self.kernel_class = Echo_Kernel
        self.kernel_spec  = Echo_Kernel_Install().kernel_spec
        self.python_kernel = Test_Server().docker().jupyter_kernel().first_or_new()

        self.kernel_install = Kernel_Install(self.kernel_name, self.kernel_class,self.kernel_spec, self.python_kernel)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_install(self):
        #assert self.kernel_install.uninstall().get('status') == 'ok'
        assert self.kernel_install.exists() is False
        assert self.kernel_install.install().get('status') == 'ok'
        assert self.kernel_install.exists() is True


class test_Echo_Kernel(TestCase):
    def setUp(self):
        self.delete_on_exit = True
        self.result         = None
        self.kernel_name    = 'Echo'
        #self.jp_cell        = Test_Server().docker().jupyter_cell()
        self.jp_echo        = Test_Server().docker().jupyter_kernel().first_or_new(self.kernel_name )
        self.echo_kernel    = Echo_Kernel()


    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.delete_on_exit:
            self.jp_echo.delete()

    def test__init__(self):
        self.result = self.jp_echo.info()

    def test___execute_on_kernel(self):
        text = 'Hello...'
        Dev.pprint(self.jp_echo.execute(text).get('stdout'))
        #assert self.jp_echo.execute(text).get('stdout') == [text]





    #
    # def test_install_and_uninstall(self):
    #
    #
    #     assert 'ok'   == self.python_kernel.execute(install_code).get('status')
    #
    #     assert "echo" in set(self.python_kernel.kernels_specs())
    #
    #     assert 'ok'   == self.python_kernel.execute(uninstall_code).get('status')
    #
    #     assert "echo" not in set(self.python_kernel.kernels_specs())
    #
    #
    #     from jupyter_client.kernelspec import KernelSpecManager
    #     #Dev.pprint(KernelSpecManager().get_all_specs())
    #     #KernelSpecManager().remove_kernel_spec('echo')
    #     #Dev.pprint(KernelSpecManager().get_all_specs())
    #
    #     #self.result = self.echo_kernel.install()
    #     #Dev.pprint(self.kernels.kernels_specs())

    def test_spec(self):
        assert self.echo_kernel.spec == { 'argv'            : [ 'python','-m',
                                                                'osbot_jupyter.kernels.Echo_Kernel',
                                                                '-f','{connection_file}'],
                                          'display_name'    : 'Echo',
                                          'language'        : 'text'}