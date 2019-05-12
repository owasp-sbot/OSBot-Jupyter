from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Live_Notebook import Live_Notebook


class test_Live_Notebook(TestCase):

    def setUp(self):
        self.short_id = '3ddc8'
        self.notebook = Live_Notebook(short_id=self.short_id, headless=False)
        self.result   = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # config methods
    def test_set_build_from_short_id(self):
        assert self.notebook.set_build_from_short_id(self.short_id) is True
        assert self.notebook.set_build_from_short_id('aaaa'       ) is False

    def test_jupyter_api(self):
        assert self.notebook.jupyter_api().version()     == {'version': '5.7.8'}
        assert set(self.notebook.jupyter_api().status()) == {'connections', 'kernels', 'last_activity', 'started'}

    def test_stop(self):
        self.result = self.notebook.set_build_from_short_id(self.short_id).stop()

    # api methods

    def test_files(self):
        self.result = self.notebook.files('scenarios')
        #contents

    def test_execute_command(self):
        path ='notebooks/setup/gsbot-invoke.ipynb'
        jp_web = self.notebook.jupyter_web()
        jp_cell = self.notebook.jupyter_cell()

        if (path in jp_web.url()) is False:
            jp_web.open(path)
        jp_cell.clear()
        jp_cell.execute("""
                            a=40+2
                            print(123)
                            a
                            """)
        self.result = jp_cell.output_wait_for_data()

    def test_execute_python(self):
        self.result = self.notebook.execute_python("""
            a=40+2
            print(123)
            a                                      """, keep_contents=None)

    def test_screenshot(self):
        self.notebook.set_build_from_short_id(self.short_id)
        self.result = self.notebook.screenshot('examples/simple-commands',800)

