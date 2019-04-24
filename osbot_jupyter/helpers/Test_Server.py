from pbx_gs_python_utils.utils.Json import Json

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_API import Jupyter_API
from osbot_jupyter.api.Jupyter_Kernel import Jupyter_Kernel
from osbot_jupyter.api.Jupyter_Session import Jupyter_Session
from osbot_jupyter.api.Jupyter_Web import Jupyter_Web
from osbot_jupyter.api.Jupyter_Web_Cell import Jupyter_Web_Cell


class Test_Server:
    def __init__(self, headless=True):
        # if mode =='docker':
        #
        # else:
        #     data = Json.load_json('/tmp/active_jupyter_server.yml')
        #     self.token = data.get('token')
        #     self.server = data.get('server')
        self.image_name      = None
        self.docker_jupyter  = None
        self.token           = None
        self.server          = None
        self.headless        = headless

    def docker(self):
        self.image_name      = 'jupyter/datascience-notebook:9b06df75e445'
        self.docker_jupyter  = Docker_Jupyter(self.image_name)
        self.token           = self.docker_jupyter.token()
        self.server          = self.docker_jupyter.server()
        return self


    def jupyter_api     (self): return Jupyter_API      (server=self.server, token=self.token                       )
    def jupyter_cell    (self): return Jupyter_Web_Cell (server=self.server, token=self.token,headless=self.headless)
    def jupyter_kernel  (self): return Jupyter_Kernel   (server=self.server, token=self.token                       )
    def jupyter_session (self): return Jupyter_Session  (server=self.server, token=self.token                       )
    def jupyter_web     (self): return Jupyter_Web      (server=self.server, token=self.token,headless=self.headless)