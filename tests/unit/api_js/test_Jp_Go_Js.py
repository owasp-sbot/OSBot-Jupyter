from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api_js.Jp_Go_Js import Jp_Go_Js
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jp_Go_Js(TestCase):
    def setUp(self):
        self.jp_go_js = Jp_Go_Js()
        self.jp_cell  = Test_Server().docker().jupyter_cell()
        self.result   = None

        #sself.jp_cell.clear().input_hide()
        #self.jp_cell.new_top()

    def tearDown(self):
       if self.result is not None:
           Dev.pprint(self.result)

    def invoke_in_jp(self, target_method, hide_input=False):
        import inspect

        class_module = target_method.__module__
        class_name   = class_module.split('.').pop()
        method_name  = target_method.__name__

        code    = """
                        %autoreload
                        from {0} import {1}
                        {2} = {1}()
                        {2}.{3}()                        
                    """.format(class_module      , class_name,
                               class_name.lower(), method_name)
        self.jp_cell.text_dedent(code).execute()
        if hide_input:
            self.jp_cell.input_hide()
        return self


    def test_add_Iframe(self):
        #url = self.jp_cell.browser().sync__url()
        #self.jp_cell.browser().sync__open(url)
        self.jp_cell.clear()
        self.invoke_in_jp(Jp_Go_Js.add_iframe)
        self.jp_cell.input_hide().new_top()
        #self.jp_cell.new_top()

    def test_invoke_method(self):
        code =  """
                    %autoreload   
                    jp_go_js = Jp_Go_Js()      
                    jp_go_js.invoke_method('add_node','123123')
                """
        self.jp_cell.delete().execute(code)

    def test_add_node(self):
        self.jp_cell.delete().execute('40+1')





