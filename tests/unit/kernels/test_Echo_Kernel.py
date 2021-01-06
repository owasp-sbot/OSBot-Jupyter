import json
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jupyter.api.Kernel_Install import Kernel_Install
from osbot_jupyter.helpers.Test_Server import Test_Server
from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel, Echo_Kernel_Install


class test_Echo_Kernel__Install(TestCase):

    def setUp(self):
        self.kernel_name    = "Echo"
        self.kernel_class   = Echo_Kernel
        self.kernel_spec    = Echo_Kernel_Install().kernel_spec
        self.python_kernel  = Test_Server().docker().jupyter_kernel().new()
        self.kernel_install = Kernel_Install(self.kernel_name, self.kernel_class,self.kernel_spec, self.python_kernel)
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        self.python_kernel.delete()

    def test_install(self):
        assert self.kernel_install.install().get('status') == 'ok'
        assert self.kernel_install.exists() is True

    def test_uninstall(self):
        #error_message = self.kernel_install.uninstall()
        #print(self.kernel_install.jupyter_kernel.decode_error(error_message))
        if self.kernel_install.exists():
            assert self.kernel_install.uninstall().get('status') == 'ok'
            assert self.kernel_install.exists() is False

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
        text = 'Hello'
        Dev.pprint(self.jp_echo.execute(text).get('stdout'))
        #assert self.jp_echo.execute(text).get('stdout') == [text]



    def test_spec(self):
        assert self.echo_kernel.spec == { 'argv'            : [ 'python','-m',
                                                                'osbot_jupyter.kernels.Echo_Kernel',
                                                                '-f','{connection_file}'],
                                          'display_name'    : 'Echo',
                                          'language'        : 'text'}





class test_Echo_Kernel_in_CodeBuild(TestCase):
    def setUp(self):
        self.headless       = False
        self.test_server    = Test_Server(self.headless).codebuild()
        #self.jupyter_api    = self.test_server.jupyter_api()
        self.jupyter_web    = self.test_server.jupyter_web()
        self.jupyter_cell   = self.test_server.jupyter_cell()
        #self.jupyter_kernel = self.test_server.jupyter_kernel().first_or_new()
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_install_upgrade_library(self):
        code =  """
                    !pip install --upgrade osbot_jupyter
                """
        print(self.jupyter_cell.execute(code) \
                  .wait(0.3).output())

    def test_available_kernels(self):
        code =  """
                    from jupyter_client.kernelspec import KernelSpecManager
                    KernelSpecManager().get_all_specs()
                """
        print(self.jupyter_cell.execute(code)       \
                                .wait(0.3).output())


    def test_install(self):
        code =  """
                    from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel, Echo_Kernel_Install
                    from osbot_jupyter.api.Kernel_Install import Kernel_Install_Inside_Jupyter
                    kernel_install = Echo_Kernel_Install()
                    kernel_name    = kernel_install.kernel_name
                    kernel_class   = kernel_install.kernel_class
                    kernel_spec    = kernel_install.kernel_spec
                    kernel_spec
                    
                    kernel_install = Kernel_Install_Inside_Jupyter(kernel_class,kernel_name, kernel_spec)
                    kernel_install.install()
                """
        print(self.jupyter_cell.execute(code) \
              .wait(0.3).output())


    def test_stop_build(self):
        self.result = self.test_server.code_build_helper.stop_all_active()