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
                    jp_go_js.invoke_method('add_node',{'key':'RISK-12'})
                    jp_go_js.invoke_method('add_node',{'key':'RISK-1', 'parent': 'RISK-12' })
                    jp_go_js.invoke_method('add_node',{'key':'RISK-2', 'parent': 'RISK-12' })
                    jp_go_js.invoke_method('add_node',{'key':'RISK-3', 'parent': 'RISK-12' })
                    
                    jp_go_js.invoke_method('add_edge',{'from':'RISK-12','to':'RISK-1' })                    
                    jp_go_js.invoke_method('expand_node','RISK-12')
                    jp_go_js.invoke_method('zoom_to_fit',None)                    
                """
        self.jp_cell.delete().execute(code)

    def test__create_from_issue(self):

        code =  """
                        %autoreload
                        import sys; sys.path.append('..')
                        from helper import *
                        root_key = 'IA-402'
                        links = issue(root_key).get('Issue Links')
                        #set(links)
                        jp_go_js.clear()
                        jp_go_js.add_node(root_key).expand_node(root_key)
                        for link_type,values in links.items():    
                                                                                     
                            for link_key in values:
                                jp_go_js.add_node(link_key)
                                jp_go_js.add_link(root_key,link_key,link_type)    
                            #    jp_go_js.add_node(value, key)
                            #jp_go_js.expand_node(key)    
                """
        self.jp_cell.delete().execute(code)

        # add_node('Risk-1');
        # add_node('Risk-2', 'Risk-1')
        # add_node('Risk-3', 'Risk-1')
        # expand_node('Risk-1')

    def test___load_src_in_browse(self):
        self.jp_cell.open(self.jp_go_js.src)





