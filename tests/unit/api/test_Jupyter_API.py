import datetime
import json
import uuid
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_API import Jupyter_API


class test_Jupyter_API(TestCase):

    def setUp(self):
        self.server         = 'http://localhost:8888'
        self.image_name     = 'jupyter/datascience-notebook:9b06df75e445'
        self.notebook_name  = 'work/test-1.ipynb'
        self.docker_jp      = Docker_Jupyter(self.image_name)
        self.token          = self.docker_jp.token()
        self.api            = Jupyter_API(server=self.server, token=self.token)
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_version(self):
        assert self.api.version().get('version') == '5.7.2'

    # this is not working
    # def test_create(self):
    #     tmp_file = 'work/{0}.txt'.format(Misc.random_string_and_numbers())
    #     self.result = self.api.create(tmp_file)

    def test_contents(self):
        self.api.contents()
        self.api.contents('work')
        self.result = self.api.contents(self.notebook_name)

    def test_kernel_execute(self):
        self.result = self.api.kernel_code_execute('40+2')


    def test_kernels(self):
        self.result = self.api.kernels()

    def test_notebook_content(self):
        self.result = self.api.notebook_content(self.notebook_name)

    def test_notebook_cells(self):
        self.result = self.api.notebook_cells(self.notebook_name)

    def test_notebook_codes_source(self):
        self.result = self.api.notebook_codes_source(self.notebook_name)

    def test_sessions(self):
        self.result = self.api.sessions()


    def test_url(self):
        assert self.api.url('aaa') == 'http://localhost:8888/api/aaa'
        assert self.api.url('/aa') == 'http://localhost:8888/api/aa'
        assert self.api.url('a/a') == 'http://localhost:8888/api/a/a'
        assert self.api.url(     ) == 'http://localhost:8888/api/'
        assert self.api.url(None ) == 'http://localhost:8888/api/'

        assert self.api.url('/api'    ) == 'http://localhost:8888/api/api'
        assert self.api.url('/api/'   ) == 'http://localhost:8888/api/'
        assert self.api.url('/api/aaa') == 'http://localhost:8888/api/aaa'
        assert self.api.url('/apiaaa' ) == 'http://localhost:8888/api/apiaaa'