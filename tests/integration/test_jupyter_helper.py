import textwrap
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.helpers.Test_Server import Test_Server


class test_jupyter_helper(TestCase):

    def setUp(self):
        self.cell  = Test_Server().docker().jupyter_cell()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_config_environment(self):
        self.cell.clear()
        code = textwrap.dedent("""
                                    %load_ext autoreload
                                    %autoreload 
                                    #%autocall 2                                    
                                    !pip install ipywidgets
                                    from helper import *
                               """)

        self.cell.execute(code)

    def test_hello(self):
        self.cell.execute('%autoreload\n'
                          'hello("steve")')

    def test_img(self):
        self.cell.execute('screenshot("https://www.google.com/asd")')

    def test_issue(self):
        self.cell.execute('issue("RISK-12")')

    def test_graph_show(self):
        self.cell.execute('graph("graph_NXW")')
