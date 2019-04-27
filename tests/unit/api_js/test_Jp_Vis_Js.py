from unittest import TestCase

from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jp_Vis_Js(TestCase):
    def setUp(self):
        self.vis_js = Jp_Vis_Js()
        self.jp_cell = Test_Server().docker().jupyter_cell()
        self.jp_cell.new_top()
        #self.jp_cell.clear().input_hide()

    def test__init__(self):         # %load_ext autoreload

        code = """                    
                    %autoreload\n
                    import sys; sys.path.append('..')
                    from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
                    jp_vis = Jp_Vis_Js()
                    jp_vis.test
               """
        self.result = self.jp_cell.execute(code)

    def test_invoke(self):
        libs = self.vis_js.libs
        js_code = "element.text(vis)"
        title = "<h1>Vis Js tests</h1>"
        self.jp_cell.execute_html(title).input_hide()

        self.jp_cell.execute_javascript_with_libs(libs, js_code).wait(0.1)
        assert self.jp_cell.output() == '[object Object]'