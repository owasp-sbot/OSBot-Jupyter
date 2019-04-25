import ipywidgets as widgets
from IPython.display import display, HTML

from IPython.display import display_html
from osbot_aws.apis.Lambda import Lambda

out = widgets.Output()

def answer():
    return 47

def hello(name):
    #out.clear_output()
    #display('Display in main thread')
    #display(out)
    return "Hi {0}, how are you felling today?".format(name)

def issue(key):
    from osbot_jira.api.API_Issues import API_Issues
    return API_Issues().issue(key)

def graph_show(graph_name):
    from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
    png_data = Lambda_Graph().get_graph_png___by_name(graph_name).get('png_base64')
    show_png(png_data)

def screenshot(url):
    print('taking screenshot of: {0}'.format(url))
    payload = {"params": ['screenshot',url]}
    png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
    print(png_data)
    show_png(png_data)

def show_png(png_data):
    html = '<img style="border:1px solid black" align="left" src="data:image/png;base64,{}"/>'.format(png_data)
    display_html(html, raw=True)

# experiments

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout