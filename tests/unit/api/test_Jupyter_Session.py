from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Jupyter_Kernel import Jupyter_Kernel
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_Session(TestCase):

    def setUp(self):
        self.notebook   = 'work/test-AAAA.ipynb'
        self.jp_session = Test_Server().docker().jupyter_session().set_to_notebook(self.notebook)
        self.result     = None

    def tearDown(self):
        if self.jp_session.exists():
            self.jp_session.delete()
        if self.result is not None:
            Dev.pprint(self.result)

    def test_info(self):
        info = self.jp_session.info()
        assert set(info) == {'kernel', 'name', 'id', 'type', 'path'}
        assert info.get('path') == self.notebook
        assert info.get('type') == 'python3'
        assert info.get('id')   == self.jp_session.session_id

        assert info.get('kernel').get('name') == 'python3'

    def test_delete(self):
        assert self.jp_session.delete() is True
        assert self.jp_session.delete() is False

    def test_rename(self):
        name        = Misc.random_string_and_numbers()
        assert self.jp_session.rename(name).get('name') == name
        assert self.jp_session.info  (    ).get('name') == name

    def test_sessions(self):
        assert len(self.jp_session.sessions()) > 0

    def test_sessions_ids(self):
        assert len(self.jp_session.sessions_ids()) > 0



