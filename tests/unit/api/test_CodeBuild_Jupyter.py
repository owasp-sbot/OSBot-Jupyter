from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper


class test_CodeBuild_Jupyter_Helper(TestCase):
    def setUp(self):
        self.api    = CodeBuild_Jupyter_Helper()
        self.result = None

    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test_get_active_build_id(self):
        self.result = self.api.get_active_build_id()

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

    def test_start_build_for_repo_and_wait_for_jupyter_load(self):
        repo = 'gs-notebook-risks'
        repo = 'gs-detect-notebooks'        
        self.result = self.api.start_build_for_repo_and_wait_for_jupyter_load(repo)


    def test_stop_all_active(self):
        result = CodeBuild_Jupyter_Helper().stop_all_active()
        Dev.pprint("stopped builds {0}".format(result))

    def test_save_active_server_details(self):
        tmp_file    = '/tmp/active_jupyter_server.yml'
        self.result = self.api.save_active_server_details(tmp_file)

class test_CodeBuild_Jupyter(TestCase):
    def setUp(self):
        self.result = None
        self.build_id = 'OSBot-Jupyter:f8119f0f-6cf9-468c-a193-f11846c4cc1d'
        self.api      = CodeBuild_Jupyter(build_id = self.build_id)


    def tearDown(self):
        if self.result:
            Dev.pprint(self.result)

    def test_start_new_build(self):
        self.build_id = CodeBuild_Jupyter_Helper().start_build_and_wait_for_jupyter_load().build_id
        print(self.build_id)
        self.api = CodeBuild_Jupyter(build_id=self.build_id)
        self.result = self.api.url()


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