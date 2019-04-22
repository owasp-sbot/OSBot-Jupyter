import base64

from osbot_aws.apis.Lambda import load_dependency

class Jupyter_Web:

    def __init__(self, token=None,headless=True):
        self.headless       = headless
        self.server         = {'schema':'http', 'ip':  '127.0.0.1' , 'port' : 8888 }
        self.token      = token
        self.tmp_screenshot = '/tmp/jupyter_screenshot.png'
        self._url           = None
        self._browser       = None  # API_Browser(headless=headless)

    def cell_execute_python(self,python_code):
        self.cell_selected_set_text(python_code)
        self.cell_selected_code_execute()
        #encoded_text = base64.b64encode(python_code.strip().encode()).decode()
        #js_script = "{0}(JSON.parse(atob('{1}')))".format(name, encoded_text)
        #js_code = """cell = Jupyter.notebook.get_selected_cell();
        #             cell.set_text(atob('{0}')) ; cell.execute() ;""".format(encoded_text)
        #self.browser().sync__js_execute(js_code)

    def cell_selected_get_text(self):
        js_code = """Jupyter.notebook.get_selected_cell().get_text()"""
        return self.browser().sync__js_execute(js_code)

    def cell_selected_set_text(self,text):
        encoded_text = base64.b64encode(text.strip().encode()).decode()
        js_code = """cell = Jupyter.notebook.get_selected_cell();
                     cell.set_text(atob('{0}'));""".format(encoded_text)
        self.browser().sync__js_execute(js_code)
        return self

    def cell_selected_js_invoke(self,js_code):
        js_code = """cell = Jupyter.notebook.get_selected_cell();
                     {0};""".format(js_code)
        self.browser().sync__js_execute(js_code)

    def cell_selected_code_execute(self): self.cell_selected_js_invoke("cell.execute()")

    def cell_append_new(self):
        js_code = """Jupyter.notebook.insert_cell_below();
                     Jupyter.notebook.select_next(true);
                     Jupyter.notebook.focus_cell();"""
        self.browser().sync__js_execute(js_code)

    # def cell_selected_to_markdown(self):
# Jupyter.notebook.cells_to_markdown() // change in ui the current cell to markdown
# Jupyter.notebook.cells_to_code() // change in ui the current cell to markdown
# Jupyter.notebook.delete_cell()
# Jupyter.notebook.get_cells()

    def browser(self):
        if self._browser is None:
            load_dependency('syncer')
            from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
            browser_helper  = Browser_Lamdba_Helper(headless=self.headless).setup()
            self._browser    = browser_helper.api_browser
        return self._browser

    def browser_width(self,width):
        self.browser().sync__browser_width(width=width)
        return self

    def current_page(self):
        return self.browser().sync__url()

    def login(self):
        return self.open('?token={0}'.format(self.token))

    def logout(self):
        return self.open('logout')

    def open(self, path):
        url = self.resolve_url(path)
        self.browser().sync__open(url)
        return self

    def open_notebook(self,notebook_path):
        return self.open('nbconvert/html/{0}.ipynb?download=false'.format(notebook_path))

    def open_notebook_edit(self, notebook_path):
        return self.open('notebooks/{0}.ipynb'.format(notebook_path))

    def open_tree(self):
        return self.open('tree')

    def screenshot(self,url=None):
        self.browser().sync__screenshot(url=url,full_page=True, file_screenshot=self.tmp_screenshot)
        return self.tmp_screenshot

    def screenshot_base64(self,url=None):
        return self.browser().sync__screenshot_base64(full_page=True,url=url)


    def resolve_url(self,path=None):
        if self._url is None:
            self._url = "{0}://{1}:{2}".format(self.server.get('schema'), self.server.get('ip'),self.server.get('port'))

        if   path is None or len(path) == 0: path = '/'
        elif path[0] != '/'                : path = '/' + path

        return "{0}{1}".format(self._url,path)

    def ui_hide_input_boxes(self):
        self.browser().sync__js_execute("$('div.input').hide()")
        return self

    def set_url  (self, value): self._url   = value; return self
    def set_token(self, value): self.token  = value; return self