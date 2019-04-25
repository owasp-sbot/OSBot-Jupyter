from unittest import TestCase

from osbot_jupyter.helpers.Test_Server import Test_Server


class test_jupyter_helper(TestCase):

    def setUp(self):
        self.cell = Test_Server().docker().jupyter_cell()

    def test_config_environment(self):
        code ="""%load_ext autoreload
                  %autoreload 
                  %autocall 2
                  from helper import *"""

        self.cell.select(1)