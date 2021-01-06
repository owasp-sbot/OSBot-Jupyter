from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jp_Vis_Js(TestCase):
    def setUp(self):
        self.vis_js = Jp_Vis_Js()
        self.jp_cell = Test_Server().docker().jupyter_cell()
        self.jp_cell.clear()#.input_hide()
        self.jp_cell.new_top()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)


    # def test__init__(self):         # %load_ext autoreload
    #
    #     code = """
    #                 %autoreload\n
    #                 import sys; sys.path.append('..')
    #                 from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
    #                 jp_vis = Jp_Vis_Js()
    #                 #jp_vis.js_invoke('element.text(vis)')
    #                 jp_vis.test_vis()
    #            """
    #     self.result = self.jp_cell.execute(code)

    def helper(self, target_class, target_method, test_method):
        import inspect

        class_module = target_class.__module__
        class_name   = target_class.__name__

        runner    = """
                        %autoreload
                        from {0} import {1}
                        target = {1}()
                        simple_graph(target)
                        simple_graph_test(target)
                    """.format(class_module, class_name)
        code      = inspect.getsource(self.vis_js.simple_graph)
        code_test = inspect.getsource(self.vis_js.simple_graph_test)

        self.jp_cell.new().text_dedent(code     ).execute()
        self.jp_cell.new().text_dedent(code_test).execute()
        self.jp_cell.new_top().text_dedent(runner   ).execute().input_hide()
        #self.result = runner

    def test_helper(self):
        self.jp_cell.delete()
        self.helper(Jp_Vis_Js, Jp_Vis_Js.simple_graph, Jp_Vis_Js.simple_graph_test)

    def test_invoke(self):
        code = """
                    jp_vis.test_vis()
               """
        import inspect
        import textwrap
        runner = """                    
                    from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
                    target = Jp_Vis_Js()
                    simple_graph(target)
                    simple_graph_test(target)
                 """


        code      = inspect.getsource(self.vis_js.simple_graph)
        code_test = inspect.getsource(self.vis_js.simple_graph_test)

        self.jp_cell      .text_dedent(code     ).execute()
        self.jp_cell.new().text_dedent(code_test).execute()
        self.jp_cell.new().text_dedent(runner   ).execute()




        #self.jp_cell.execute(code)