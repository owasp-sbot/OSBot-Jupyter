from pycallgraph.output import GraphvizOutput
from pycallgraph import Color
from pycallgraph import Config
from pycallgraph import PyCallGraph
from pycallgraph import GlobbingFilter

class Trace_Call:

    def __init__(self, img_file = None):
        self.img_file = img_file
        if self.img_file is None:  self.img_file  = '/tmp/trace_PyCallGraph.png'
        self.graphviz             = GraphvizOutput()
        self.graphviz.output_file = self.img_file
        self.include_filter       = ['osbot*', 'pbx*'] #, 'boto3*'

    def rainbow(node):
        return Color.hsv(node.time.fraction * 0.8, 0.4, 0.9)

    def greyscale(node):
        return Color.hsv(0, 0, node.time.fraction / 2 + 0.4)

    def orange_green(node):
        return Color(0.2 + node.time.fraction * 0.8,
                     0.2 + node.calls.fraction * 0.4,
                     0.2)


    def invoke_method(self, method, *params):
        self.graphviz.edge_color_func = lambda e: Color(0, 0, 0)
        # graphviz.node_color_func = rainbow #orange_green # greyscale

        config = Config(include_stdlib=True)  # max_depth=10)

        config.trace_filter = GlobbingFilter(include=self.include_filter)

        with PyCallGraph(output=self.graphviz, config=config):
            try:
                return_value = method(*params)
                return { 'status'  : 'ok'          ,
                         'data'    : return_value  ,
                         'img_file': self.img_file }

            except Exception as error:
                return {'status':'error', 'data': '{0}'.format(error)}
