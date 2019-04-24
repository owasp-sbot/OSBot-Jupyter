from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Jupyter_Kernel import Jupyter_Kernel
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_Session(TestCase):

    def setUp(self):
        self.jp_session = Test_Server().docker().jupyter_session()
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_session(self):
        session_id = Misc.array_pop(self.api.sessions_ids())
        self.result = self.api.session(session_id)

    def test_session_get(self):
        self.api.session_delete_all()
        notebook = 'work/test-1.ipynb'
        self.result = self.api.session_get(notebook)

    def test_session_delete(self):
        session_id  = Misc.array_pop(self.api.sessions_ids())

        assert self.api.session_delete(session_id) is True
        assert self.api.session_delete(session_id) is False

    def test_session_rename(self):
        name        = Misc.random_string_and_numbers()
        session_id  = self.api.sessions_ids()[0]
        assert self.api.session_rename(session_id, name).get('name') == name
        assert self.api.session       (session_id      ).get('name') == name

        #self.result = self.api.session(session_id)


    def test_sessions(self):
        assert len(self.jp_session.sessions()) > 0

    def test_sessions_ids(self):
        assert len(self.jp_session.sessions_ids()) > 0



