import base64
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.osbot.Jupyter_Web_Commands import Jupyter_Web_Commands


class test_Jupyter_Web_Commands(TestCase):

    def setUp(self):
        self.short_id    = '42117'
        self.result      = None
        self.png_data    = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

        if self.png_data:
            png_file = '/tmp/lambda_png_file.png'
            with open(png_file, "wb") as fh:
                fh.write(base64.decodebytes(self.png_data.encode()))
            Dev.pprint("Png data with size {0} saved to {1}".format(len(self.png_data), png_file))

    def test_screenshot(self):
        params = [self.short_id]
        self.png_data = Jupyter_Web_Commands.screenshot(None,None, params)