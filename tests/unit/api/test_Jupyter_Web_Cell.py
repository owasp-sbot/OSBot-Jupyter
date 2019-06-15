import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev      import Dev
from pbx_gs_python_utils.utils.Misc     import Misc
from osbot_jupyter.helpers.Test_Server  import Test_Server


class test_Jupyter_Web_Cell(TestCase):

    def setUp(self):
        self.headless    = False
        #self.cell        = Test_Server(self.headless).docker().jupyter_cell()
        self.test_Server = Test_Server(self.headless).codebuild()
        self.jp_web      = self.test_Server.jupyter_web()
        self.jp_cell     = self.test_Server.jupyter_cell()
        #self.jp          = Test_Server(self.headless).docker().jupyter_web()
        self.result      = None
        #self.jp_cell.clear().text('Unit Test execution will go below')

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # check test environment
    def test_jp_web_open_page(self):
        notebook_path = 'users/gsbot/gsbot-invoke.ipynb'
        self.jp_web.login()
        self.jp_web.open_notebook(notebook_path)

    def test_jp_web_edit_page(self):
        notebook_path = 'users/gsbot/gsbot-invoke'
        self.jp_web.open_notebook_edit(notebook_path)

    def test_jp_cell_clear_and_test_text(self):
        self.jp_cell.clear().text('Unit Test execution will go below')

    # methods
    def test_delete(self):
        self.jp_cell.new().text('to delete').delete()

    def test_new(self):
        text  = 'new text'
        assert self.jp_cell.new().text(text).text() == text

    def test_execute_html(self):
        html = "<h1>{0}</h1>".format(Misc.random_string_and_numbers())
        (
            self.jp_cell.execute_html(html).wait(0.1)
                     .output_hide()     .wait(0.2)
                     .output_show()
        )
        assert self.jp_cell.output_html().strip() == html

    @unittest.skip('fix: needs a better way to capture this data from output')
    def test_execute_javascript(self):
        js_code = "element.text(40+2)"
        self.jp_cell.execute_javascript(js_code).wait(0.1)
        assert self.jp_cell.output().strip() == '42'

    def test_execute_javascript_with_libs(self):
        libs = [{ 'lib_name': 'jquery', 'url':'https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js'},
                { 'lib_name': 'vis'   , 'url':'https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js'    }]
        js_code = "element.text(vis + jquery)"
        self.jp_cell.execute_javascript_with_libs(libs,js_code).wait(0.3)
        assert self.jp_cell.output() == '[object Object]function(e,t){return new w.fn.init(e,t)}'

    def test_execute_python(self):
        python_code = """
                        a = 40+2
                        print(str(a) + "_double_" + 'single')
                        a"""

        self.jp_cell.execute(python_code)

    def test_text_get_value(self):
        self.result = self.jp_cell.select(0).text()

    def test_text_set_value(self):
        text = Misc.random_string_and_numbers()
        self.jp_cell.select(0).text(text)
        assert self.jp_cell.text() == text

    def test_cell_select(self):
        self.jp_cell.select(0)
        self.jp_cell.select(1)
        self.jp_cell.select(2)
        self.jp_cell.select(3)

    def test_input_hide__input_show(self):
        self.jp_cell.input_hide().wait(0.01).input_show()

    def test_to_markdown(self):
        Dev.pprint(self.token)
        self.jp_cell.new().to_markdown().text('# an title 123').execute().wait(1).delete()

    def test_to_code(self):
        self.jp_cell.new().to_markdown().to_code().text('"an title 123"').execute()#.wait(1).delete()