import base64
from time import sleep

from osbot_jupyter.api.Jupyter_Web import Jupyter_Web


class Jupyter_Web_Cell(Jupyter_Web):

    def __init__(self, token=None, server=None, headless=True):
        super().__init__(token=token, server=server, headless=headless)

    def execute_python(self,python_code, new_cell=True, delete_after=False):
        if new_cell:
            self.new();
        self.text(python_code)
        self.execute()
        if delete_after:
            self.delete()

    def js_invoke(self,js_code):
        return self.browser().sync__js_execute(js_code)

    def new(self):
        js_code = """Jupyter.notebook.insert_cell_below();
                     Jupyter.notebook.select_next(true);
                     Jupyter.notebook.focus_cell();"""
        self.browser().sync__js_execute(js_code)
        return self

    def text(self,value=None):
        if value is None:
            js_code = "Jupyter.notebook.get_selected_cell().get_text()"
            return self.browser().sync__js_execute(js_code)
        else:
            encoded_text = base64.b64encode(value.strip().encode()).decode()
            js_code = """cell = Jupyter.notebook.get_selected_cell();
                         cell.set_text(atob('{0}'));""".format(encoded_text)
            self.browser().sync__js_execute(js_code)
            return self


    def wait(self,seconds):
        sleep(seconds)
        return self

    def delete      (self       ): self.js_invoke("Jupyter.notebook.delete_cell()"             ); return self
    def execute     (self       ): self.js_invoke("Jupyter.notebook.execute_cell()"            ); return self
    def select      (self,index ): self.js_invoke("Jupyter.notebook.select({0})".format(index )); return self
    def to_markdown (self       ): self.js_invoke("Jupyter.notebook.cells_to_markdown()"       ); return self
    def to_code     (self       ): self.js_invoke("Jupyter.notebook.cells_to_code()"           ); return self



    # def cell_selected_to_markdown(self):
# Jupyter.notebook.cells_to_markdown() // change in ui the current cell to markdown
# Jupyter.notebook.cells_to_code() // change in ui the current cell to markdown
# Jupyter.notebook.delete_cell()
# Jupyter.notebook.get_cells()