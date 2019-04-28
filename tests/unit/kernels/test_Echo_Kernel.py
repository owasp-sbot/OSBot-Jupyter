from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
from osbot_jupyter.helpers.Test_Server import Test_Server
from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel


class test_Jp_Vis_Js(TestCase):
    def setUp(self):
        self.delete_on_exit = True
        self.result         = None
        self.kernel_name    = 'Echo'
        self.vis_js         = Jp_Vis_Js()
        self.jp_cell        = Test_Server().docker().jupyter_cell()
        self.python_kernel  = Test_Server().docker().jupyter_kernel().first_or_new()
        self.echo_kernel    = Echo_Kernel()


    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.delete_on_exit:
            self.python_kernel.delete()

    def test_install_and_uninstall(self):

        install_code =    """
                              from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel                    
                              Echo_Kernel().install()
                          """
        uninstall_code =  """
                              from osbot_jupyter.kernels.Echo_Kernel import Echo_Kernel                    
                              Echo_Kernel().uninstall()
                          """
        assert 'ok'   == self.python_kernel.execute(install_code).get('status')

        assert "echo" in set(self.python_kernel.kernels_specs())

        assert 'ok'   == self.python_kernel.execute(uninstall_code).get('status')

        assert "echo" not in set(self.python_kernel.kernels_specs())


        from jupyter_client.kernelspec import KernelSpecManager
        #Dev.pprint(KernelSpecManager().get_all_specs())
        #KernelSpecManager().remove_kernel_spec('echo')
        #Dev.pprint(KernelSpecManager().get_all_specs())

        #self.result = self.echo_kernel.install()
        #Dev.pprint(self.kernels.kernels_specs())

    def test_spec(self):
        assert self.echo_kernel.spec == { 'argv'            : [ 'python','-m',
                                                                'osbot_jupyter.kernels.Echo_Kernel',
                                                                '-f','{connection_file}'],
                                          'display_name'    : 'Echo',
                                          'language'        : 'text'}