from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter
from osbot_jupyter.api.Jupyter_Web import Jupyter_Web
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter(TestCase):

    def setUp(self):
        self.headless   = False
        #data             = Json.load_json('/tmp/active_jupyter_server.yml')
        #self.token       = data.get('token')
        #self.server      = data.get('server')
        #self.jp          = Jupyter_Web(token=self.token, server=self.server, headless=self.headless)
        self.jp          = Test_Server(self.headless).docker().jupyter_web()
        self.server      = self.jp.server
        self.result      = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert type(self.jp).__name__ == 'Jupyter'
        assert self.jp.server == {'schema': 'http', 'ip': '127.0.0.1' , 'port' : 8888}


    def test_current_page(self):
        self.result = self.jp.current_page()

    def test_login(self):
        self.jp.logout()                                                               # log out user
        assert self.jp.current_page() == '{0}/logout'.format(self.server)              # confirm we are in logout page
        self.jp.open_tree()                                                            # try to open tree page
        assert self.jp.current_page() == '{0}/login?next=%2Ftree'.format(self.server)  # confirm redirect to login
        self.jp.login()                                                                # log in user
        assert self.jp.current_page() == '{0}/tree'.format(self.server)                # confirm now on tree page

    def test_open_notebook(self):
        notebook_path = 'work/test-1'
        self.jp.open_notebook(notebook_path)
        assert self.jp.current_page() == '{0}/nbconvert/html/{1}.ipynb?download=false'.format(self.server,notebook_path)

    def test_open_notebook_edit(self):
        self.jp.open_notebook_edit('work/test-1')
        assert self.jp.current_page() == '{0}/notebooks/work/test-1.ipynb'.format(self.server)

    def test_open_tree(self):
        assert self.jp.open_tree().current_page() == 'http://127.0.0.1:8888/tree'

    def test_screenshot(self):
        #target  = 'work/with-slider'
        target = 'work/test-1'
        (
            self.jp.login()
                   .open_notebook(target)
                   .ui_hide_input_boxes()
                   #.browser_width(1200)
                   .screenshot()
        )
        assert Files.exists(self.jp.tmp_screenshot)

    def test_resolve_url(self):
        assert self.jp.resolve_url('/aaa') == 'http://127.0.0.1:8888/aaa'
        assert self.jp.resolve_url('/a/b') == 'http://127.0.0.1:8888/a/b'
        assert self.jp.resolve_url('aaaa') == 'http://127.0.0.1:8888/aaaa'
        assert self.jp.resolve_url('a/bb') == 'http://127.0.0.1:8888/a/bb'
        assert self.jp.resolve_url(''    ) == 'http://127.0.0.1:8888/'
        assert self.jp.resolve_url(      ) == 'http://127.0.0.1:8888/'
        assert self.jp.resolve_url(None  ) == 'http://127.0.0.1:8888/'



    # def test_browser_screenshot(self):
    #     self.jp = Jupyter('fb3659fa3a46118fcc341e2630a9250a1402077260553436')
    #     self.jp.server = {'schema':'https', 'ip':  '421bad3b.ngrok.io' , 'port' : 443 }
    #
    #
    #     self.jp.login()
    #     self.jp.browser_width(1000)
    #     self.jp.open_notebook('gsbot-experiements').screenshot()
