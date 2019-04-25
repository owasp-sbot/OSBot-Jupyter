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


def screenshot(url):
    payload = {"params": ['screenshot',url]}
    png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
    show_png(png_data)

def show_png(png_data):
    html = '<img style="margin:0" align="left" src="data:image/png;base64,{}"/>'.format(png_data)
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