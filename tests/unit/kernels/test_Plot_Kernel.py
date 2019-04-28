from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Jupyter_Kernel import Jupyter_Kernel
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Plot_Kernel(TestCase):

    def setUp(self):
        self.delete_on_exit = True
        self.result         = None
        self.kernel_name    = 'Plotter'
        self.kernel         = Test_Server().docker().jupyter_kernel().first_or_new(self.kernel_name)

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.delete_on_exit:
            self.kernel.delete()


    def test___setup(self):
        info = self.kernel.info()
        assert info['connections'    ] == 0
        assert info['execution_state'] in ['starting','idle']
        assert info['name'           ] == self.kernel_name

    def test_kernel_execute(self):
        code = 'y=tan(x*10)'
        result = self.kernel.execute(code)
        display_data = result.get('display_data')
        assert set(display_data[0]) == {'source', 'metadata', 'data'}
        del display_data[0]
        assert result == {  'display_data'  : [],
                            'input'         : 'y=tan(x*10)',
                            'output'        : None,
                            'status'        : 'ok',
                            'stdout'        : ['Plotting 1 function(s)', 'Hello (this is a custom message)'],
                            'stream'        : [],
                            'unhandled'     : []}

    def test_kernel_spec(self):
        spec = self.kernel.kernels_specs().get(self.kernel_name.lower())

        assert spec == { 'name': 'plotter',
                         'resources': {},
                         'spec': { 'argv'         : [ 'python','-m',
                                                      'osbot_jupyter.kernels.PlotKernel',
                                                      '-f','{connection_file}'],
                                  'display_name'  : 'Plotter',
                                  'env'           : {},
                                  'interrupt_mode': 'signal',
                                  'language'      : 'python',
                                  'metadata'      : {}}}

