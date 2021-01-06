from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Json import Json

from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from osbot_jupyter.api.Jupyter_API import Jupyter_API
from osbot_jupyter.api.Jupyter_Web import Jupyter_Web
from osbot_jupyter.api.Jupyter_Web_Cell import Jupyter_Web_Cell
from osbot_jupyter.api.Jypyter_API_Actions import Jupyter_API_Actions


class test_jupyter_dev_coding(TestCase):

    def setUp(self):
        self.headless       = False
        #self.server         = 'http://localhost:8888'
        #self.image_name     = 'jupyter/datascience-notebook:9b06df75e445'
        self.notebook_name  = 'work/test-1.ipynb'
       # self.docker_jp      = Docker_Jupyter(self.image_name)
       # self.token          = self.docker_jp.token()
        data                = Json.load_file('/tmp/active_jupyter_server.yml')
        self.token          = data.get('token')
        self.server         = data.get('server')
        self.jp_api         = Jupyter_API_Actions(server=self.server, token=self.token)
        self.jp_web         = Jupyter_Web_Cell(token=self.token, headless=self.headless)
        self.jp_cell        = Jupyter_Web_Cell(token=self.token, headless=self.headless)
        self.notebook_name  = 'dev_coding'
        self.notebook_path  = '{0}.ipynb'.format(self.notebook_name)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)


    def test_open_dev_notebook(self):
        if self.jp_api.notebook_exists(self.notebook_path) is False:
            self.jp_api.create_notebook(notebook_name=self.notebook_name)
        self.jp_web.open_notebook_edit(self.notebook_name)

    def test_set_dev_environment(self):
        code = "%load_ext autoreload\n%autoreload 2"
        self.jp_cell.execute_python(code)
        self.jp_cell.delete()

    def test_run_code(self):
        code = """
from osbot_jupyter.notebook.Widgets import Widgets
Widgets().ping()
        """

        self.jp_cell.execute_python(code, new_cell=False)


    def test_add_code_hide_button(self):
        code = """
from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')        
"""

        self.jp_cell.execute_python(code, new_cell=True)

class test_start_code_build_environment(TestCase):

    def test_create(self):
        headless = False
        file     = '/tmp/active_jupyter_server.yml'
        api      = CodeBuild_Jupyter_Helper()
        #result   = api.start_build_and_wait_for_jupyter_load()
        #build_id = api.get_active_build_id()
        config   = api.save_active_server_details(file)
        #Dev.pprint(result.build_status())
        #Dev.pprint(build_id)
        Dev.pprint(config)
        jp_web = Jupyter_Web(token=config.get('token'), server=config.get('server'), headless=headless)
        jp_web.login()
        jp_api = Jupyter_API(token=config.get('token'), server=config.get('server'), headless=headless)

