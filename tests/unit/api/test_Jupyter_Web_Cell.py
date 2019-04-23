from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_Web_Cell import Jupyter_Web_Cell


class test_Jupyter_Web_Cell(TestCase):

    def setUp(self):
        self.headless = False
        self.image_name = 'jupyter/datascience-notebook:9b06df75e445'
        self.docker_jp  = Docker_Jupyter(self.image_name)
        self.token      = self.docker_jp.token()
        self.cell       = Jupyter_Web_Cell(token=self.token, headless=self.headless)
        self.result     = None

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
        self.cell.new().to_markdown().text('# an title 123').execute().wait(1).delete()

    def test_to_code(self):
        self.cell.new().to_markdown().to_code().text('"an title 123"').execute()#.wait(1).delete()