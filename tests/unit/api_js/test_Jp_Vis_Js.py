from unittest import TestCase

from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jp_Vis_Js(TestCase):
    def setUp(self):
        self.vis_js = Jp_Vis_Js()
        self.jp_cell = Test_Server().docker().jupyter_cell()
        self.jp_cell.clear()

    def test_connectivity(self):
        self.jp_cell.execute_html("<h1>asda</h1>")

