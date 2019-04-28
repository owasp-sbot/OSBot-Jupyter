from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Kernel_Install import Kernel_Install
from osbot_jupyter.helpers.Test_Server import Test_Server
from osbot_jupyter.kernels.GSBot_Kernel import GSBot_Kernel_Install


class test_GSBot_Kernel_Install(TestCase):

    def setUp(self):

        self.gsbot_install  = GSBot_Kernel_Install()
        self.kernel_name    = self.gsbot_install.kernel_name
        self.kernel_spec    = self.gsbot_install.kernel_spec
        self.kernel_class   = self.gsbot_install.kernel_class
        self.python_kernel  = Test_Server().docker().jupyter_kernel().new()
        self.kernel_install = Kernel_Install(self.kernel_name, self.kernel_class,self.kernel_spec, self.python_kernel)
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        self.python_kernel.delete()

    def test_install(self):
        #self.result = self.kernel_install.install()
        assert self.kernel_install.install().get('status') == 'ok'
        assert self.kernel_install.exists() is True

    def test_uninstall(self):
        if self.kernel_install.exists():
            assert self.kernel_install.uninstall().get('status') == 'ok'
            assert self.kernel_install.exists() is False

    def test_uninstall_and_install(self):
        assert self.kernel_install.uninstall().get('status') == 'ok'
        assert self.kernel_install.install  ().get('status') == 'ok'

class test_GSBot_Kernel(TestCase):
    def setUp(self):
        self.delete_on_exit = True
        self.result         = None
        self.kernel_name    = 'GSBot'
        self.jp_gsbot       = Test_Server().docker().jupyter_kernel().first_or_new(self.kernel_name )


    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)
        if self.delete_on_exit:
            self.jp_gsbot.delete()

    def test__init__(self):
        self.result = self.jp_gsbot.info()

    def test___execute_on_kernel(self):
        text = 'hello'
        Dev.pprint(self.jp_gsbot.execute(text).get('stdout'))
        #assert self.jp_echo.execute(text).get('stdout') == [text]

    def test___execute_on_kernel__jira_version(self):
        text = 'jira version'
        Dev.pprint(self.jp_gsbot.execute(text).get('stdout'))


    def test___execute_on_kernel__jira_links(self):
        text = 'jira links RISK-12 all 1'
        Dev.pprint(self.jp_gsbot.execute(text).get('stdout'))
