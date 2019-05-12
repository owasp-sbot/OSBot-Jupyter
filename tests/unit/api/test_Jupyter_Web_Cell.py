import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev      import Dev
from pbx_gs_python_utils.utils.Misc     import Misc
from osbot_jupyter.helpers.Test_Server  import Test_Server


class test_Jupyter_Web_Cell(TestCase):

    def setUp(self):
        self.headless = False
        self.cell        = Test_Server().docker().jupyter_cell()
        self.result      = None
        self.cell.clear().text('Unit Test execution will go below')

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_delete(self):
        self.cell.new().text('to delete').delete()

    def test_new(self):
        text  = 'new text'
        assert self.cell.new().text(text).text() == text

    def test_execute_html(self):
        html = "<h1>{0}</h1>".format(Misc.random_string_and_numbers())
        (
            self.cell.execute_html(html).wait(0.1)
                     .output_hide()     .wait(0.2)
                     .output_show()
        )
        assert self.cell.output_html().strip() == html

    @unittest.skip('fix: needs a better way to capture this data from output')
    def test_execute_javascript(self):
        js_code = "element.text(40+2)"
        self.cell.execute_javascript(js_code).wait(0.1)
        assert self.cell.output().strip() == '42'

    def test_execute_javascript_with_libs(self):
        libs = [{ 'lib_name': 'jquery', 'url':'https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js'},
                { 'lib_name': 'vis'   , 'url':'https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js'    }]
        js_code = "element.text(vis + jquery)"
        self.cell.execute_javascript_with_libs(libs,js_code).wait(0.3)
        assert self.cell.output() == '[object Object]function(e,t){return new w.fn.init(e,t)}'

    def test_execute_python(self):
        python_code = """
                        a = 40+2
                        print(str(a) + "_double_" + 'single')
                        a"""

        self.cell.execute(python_code)

    def test_text(self):
        text = Misc.random_string_and_numbers()
        self.cell.select(0).text(text)
        assert self.cell.text() == text

    def test_cell_select(self):
        self.cell.select(0)
        self.cell.select(1)
        self.cell.select(2)
        self.cell.select(3)

    def test_input_hide__input_show(self):
        self.cell.input_hide().wait(0.01).input_show()

    def test_to_markdown(self):
        Dev.pprint(self.token)
        self.cell.new().to_markdown().text('# an title 123').execute().wait(1).delete()

    def test_to_code(self):
        self.cell.new().to_markdown().to_code().text('"an title 123"').execute()#.wait(1).delete()