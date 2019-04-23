from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_Web_Cell import Jupyter_Web_Cell
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_Web_Cell(TestCase):

    def setUp(self):
        self.headless = False
        self.cell        = Test_Server('docker').jupyter_cell()
        self.result      = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_delete(self):
        self.cell.new().text('to delete').delete()

    def test_new(self):
        text  = 'new text'
        assert self.cell.new().text(text).text() == text


    def test_execute_python(self):
        python_code = """
a = 40+2
print(str(a) + "_double_" + 'single')
a"""
        self.cell.execute_python(python_code)

    def test_text(self):
        text = Misc.random_string_and_numbers()
        self.cell.select(0).text(text)
        assert self.cell.text() == text

    def test_cell_select(self):
        self.cell.select(0)
        self.cell.select(1)
        self.cell.select(2)
        self.cell.select(3)

    def test_to_markdown(self):
        Dev.pprint(self.token)
        self.cell.new().to_markdown().text('# an title 123').execute().wait(1).delete()

    def test_to_code(self):
        self.cell.new().to_markdown().to_code().text('"an title 123"').execute()#.wait(1).delete()


    # misc use cases

    def test_login(self):
        self.cell.login()