import base64
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Live_Notebook import Live_Notebook


class test_Live_Notebook(TestCase):

    def setUp(self):
        self.short_id      = '12d62'
        self.notebook      = Live_Notebook(short_id=self.short_id, headless=True)
        self.test_notebook ='notebooks/users/gsbot/gsbot-invoke.ipynb'
        self.result        = None
        self.png_data      = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))


    # config methods
    def test_set_build_from_short_id(self):

        assert self.notebook.set_build_from_short_id(self.short_id) is self.notebook
        assert self.notebook.set_build_from_short_id('aaaa'       ) is None

        assert self.notebook.set_build_from_short_id('gscs'       ) is self.notebook  # will need this server to be running
        assert self.notebook.set_build_from_short_id('aaaa'       ) is None


    def test_jupyter_api(self):
        assert self.notebook.jupyter_api().version()     == {'version': '5.7.8'}
        assert set(self.notebook.jupyter_api().status()) == {'connections', 'kernels', 'last_activity', 'started'}

    def test_stop(self):
        self.result = self.notebook.set_build_from_short_id(self.short_id).stop()

    # api methods

    def test_files(self):
        self.result = self.notebook.files('users')
        #contents

    def test_execute_command(self):
        jp_web = self.notebook.jupyter_web()
        jp_cell = self.notebook.jupyter_cell()
        #jp_web.login()
        if (self.test_notebook in jp_web.url()) is False:
            jp_web.open(self.test_notebook)
        jp_cell.clear()
        jp_cell.execute("""
                            answer=40+2
                            print('this was executed from an unit test')
                            answer
                            """)
        self.result = jp_cell.output_wait_for_data()

    def test_execute_python(self):
        self.result = self.notebook.execute_python("""
            a=40+2
            print(123)
            a                                      """, keep_contents=None)

    def test_screenshot(self):
        self.notebook.set_build_from_short_id(self.short_id)
        self.png_data = self.notebook.screenshot(self.test_notebook,800)



    def test_bug_screenshot_duplicates_first_page(self):
        target_notebook = 'nbconvert/html/users/dinis/rdf/part-1-loading-the-rdf-file.ipynb?download=false'
        #jp_web        = self.notebook.jupyter_web()
        #jp_web.open(self.notebook)
        self.png_data = self.notebook.screenshot(target_notebook, 2000,10000)

