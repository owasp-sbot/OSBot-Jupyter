import json

import ipywidgets as widgets
import pandas     as pd
import qgrid

from IPython.display            import display_html
from osbot_gsuite.apis.GSheets  import GSheets
from osbot_aws.apis.Lambda      import Lambda

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


def jira_links(start, direction, depth):
    view = None
    lambda_graph = Lambda('osbot_jira.lambdas.jira')

    payload = {"params": ['links', start, direction, depth, view]}
    result = lambda_graph.invoke(payload)
    return json.loads(result.get('text'))

# pandas

def data_frame(data, columns):
    return pd.DataFrame(data,columns=columns)

# Multiple graph views
def graph(graph_name):
    print('creating plantuml graph for: {0}'.format(graph_name))
    from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
    png_data = Lambda_Graph().get_graph_png___by_name(graph_name).get('png_base64')
    show_png(png_data)

def mindmap(graph_name):
    print('creating mindmap graph for: {0}'.format(graph_name))
    payload = {"params": ['go_js', graph_name, 'mindmap']}
    png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
    show_png(png_data)

def viva_graph(graph_name):
    print('creating viva graph for: {0}'.format(graph_name))
    payload = {"params": ['viva_graph', graph_name, 'default']}
    png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
    show_png(png_data)

def screenshot(url):
    print('taking screenshot of: {0}'.format(url))
    payload = {"params": ['screenshot',url]}
    png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
    show_png(png_data)

def show_png(png_data):
    html = '<img style="border:1px solid black" align="left" src="data:image/png;base64,{}"/>'.format(png_data)
    display_html(html, raw=True)

def search(query,columns=None):
    params = {'params': ['search'] + query.split(' ')}
    results = Lambda("osbot_jira.lambdas.elk_to_slack").invoke(params) #{'params': ['search', 'people', 'd*']})
    return data_frame(results,columns)

# sheets and edit

def data_grid(df):
    return qgrid.show_grid(df, show_toolbar=True)

def sheet_data(file_id, sheet_name,columns=None):
    gsuite_secret_id = 'gsuite_gsbot_user'
    gsheets = GSheets(gsuite_secret_id)
    # gsheets.sheets_metadata(file_id)
    values = gsheets.get_values_as_objects(file_id, sheet_name)
    return data_frame(values, columns)

# # experiments
#
# from contextlib import contextmanager
# import sys, os
#
# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         old_stdout = sys.stdout
#         sys.stdout = devnull
#         try:
#             yield
#         finally:
#             sys.stdout = old_stdout