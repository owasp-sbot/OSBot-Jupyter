from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jypyter_API_Actions import Jupyter_API_Actions


class test_Jupyter_API_Actions(TestCase):

    def setUp(self):
        self.server     = 'http://localhost:8888'
        self.image_name = 'jupyter/datascience-notebook:9b06df75e445'
        self.docker_jp  = Docker_Jupyter(self.image_name)
        self.token      = self.docker_jp.token()
        self.api        = Jupyter_API_Actions(self.server, self.token)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_create_notebook(self):
        notebook_name = Misc.random_string_and_numbers().lower()
        notebook_path = 'work/{0}.ipynb'.format(notebook_name)
        self.result = self.api.create_notebook(notebook_name)
        assert self.api.notebook_exists(notebook_path)
