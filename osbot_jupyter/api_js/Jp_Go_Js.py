import json

from IPython.display import display, HTML, Javascript,IFrame
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Go_Js:

    def __init__(self):
        self.frame_id = Misc.random_string_and_numbers(prefix='go_view_')
        self.frame_id = 'go_view_12345'
        self.src      = '/view/html/go-js/incremental-tree.html'
        pass

    def add_iframe(self):
        iframe_code = "<iframe id='{0}' src='{1}' width='{2}' height='{3}'></iframe>".format(
                        self.frame_id, self.src, 800,300)
        display(HTML(iframe_code))
        display(Javascript("$('.output_stderr').hide()"))

        #display(IFrame(src=self.src, width=800, height=300,id=self.frame_id, abc="aaaaa" ))

    def invoke_method(self, js_method, params=None):
        data = json.dumps({'method': js_method, 'params': params})

        js_code = "{0}.contentWindow.iframe.contentWindow.postMessage({1}, '*')".format(self.frame_id, data)
        #print(self.frame_id)s
        #print(js_code)
        display(Javascript(js_code))

    def clear(self):
        self.invoke_method('clear_diagram')
        return self

    def add_node(self,key):
        self.invoke_method('add_node', {'key': key, 'label': key,'rootdistance':2})
        #print(json.dumps({'key': key, 'label': key,'rootdistance':2}))
        return self

    def add_link(self, from_key,to_key,label):
        #jp_go_js.invoke_method('add_link',{'from':'RISK-12','to':'RISK-1' ,'text':'aaaa'})
        self.invoke_method('add_link', {'from': from_key, 'to': to_key, 'text':label})
        #print(json.dumps({'from': from_key, 'to': to_key, 'text':label}))
        return self


    def expand_node(self,key):
        self.invoke_method('expand_node', key)
        return self

    def zoom_to_fit(self):
        self.invoke_method('zoom_to_fit')

        #jp_go_js.invoke_method('add_node', {'key': 'RISK-1', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-2', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-3', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('expand_node', 'RISK-12')

    # usefull JS queries

    # myDiagram.model.addNodeData({'key':'RISK-12'})
    # node = myDiagram.findNodeForKey("RISK-12");
    # node.diagram.commandHandler.expandTree(node)
    # node.diagram.commandHandler.collapseTree()