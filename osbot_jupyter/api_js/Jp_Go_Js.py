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

        #display(IFrame(src=self.src, width=800, height=300,id=self.frame_id, abc="aaaaa" ))

    def invoke_method(self, js_method, params):
        data = json.dumps({'method': js_method, 'params': params})

        js_code = "{0}.contentWindow.iframe.contentWindow.postMessage({1}, '*')".format(self.frame_id, data)
        #print(self.frame_id)s
        #print(js_code)
        display(Javascript(js_code))
