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
                     #.output_hide()     .wait(0.2)
                     #.output_show()
        )
        assert self.cell.output_html().strip() == html

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

    def test_input_hide__input_show(self):
        self.cell.input_hide().wait(0.01).input_show()

    def test_to_markdown(self):
        Dev.pprint(self.token)
        self.cell.new().to_markdown().text('# an title 123').execute().wait(1).delete()

    def test_to_code(self):
        self.cell.new().to_markdown().to_code().text('"an title 123"').execute()#.wait(1).delete()


    # misc use cases

    def test_login(self):
        self.cell.login()