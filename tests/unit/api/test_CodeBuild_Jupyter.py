from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter,CodeBuild_Jupyter_Helper

class test_CodeBuild_Jupyter_Helper(TestCase):
    def setUp(self):
        self.api    = CodeBuild_Jupyter_Helper()
        self.result = None

    def test_get_active_builds(self):
        builds = self.api.get_active_builds()
        print()
        for id, build in builds.items():
            #assert build.build_status() == 'IN_PROGRESS'
            #assert build.build_phase() == 'BUILD'             # need to improve the resilience of this test
            print(id, build.build_status() , build.build_phase())

    def test_start_build(self):
        result = self.api.start_build()
        Dev.pprint(result.build_info())

    def test_start_build_and_wait_for_jupyter_load(self):
        result = self.api.start_build_and_wait_for_jupyter_load()
        Dev.pprint(result.build_status())

    def test_stop_all_active(self):
        result = CodeBuild_Jupyter_Helper().stop_all_active()
        Dev.pprint(result)


class test_CodeBuild_Jupyter(TestCase):
    def setUp(self):
        self.result = None
        self.build_id = 'OSBot-Jupyter:745d2a4e-fdf5-4119-8b56-21b55fe9bbb5'
        self.build_id = CodeBuild_Jupyter_Helper().start_build_and_wait_for_jupyter_load().build_id
        print(self.build_id)
        self.api      = CodeBuild_Jupyter(build_id = self.build_id)


    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test_build_info(self):
        self.result = self.api.build_info()

    def test_build_status__build_phase(self):
        assert self.api.build_status() == 'IN_PROGRESS'
        assert self.api.build_phase() == 'BUILD'

    def test_build_log_messages(self):
        messages = self.api.build_log_messages()
        assert 'Waiting for agent ping' in messages.pop(0)

    def test_get_server_details_from_logs(self):
        self.result = self.api.get_server_details_from_logs()

    def test_build_stop(self):
        assert self.api.build_stop() == 'STOPPED'

    def test_url(self):
        self.result = self.api.url()