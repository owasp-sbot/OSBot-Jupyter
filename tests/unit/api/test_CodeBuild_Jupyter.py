from unittest import TestCase

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.CodeBuild import CodeBuild
from osbot_utils.utils.Dev import Dev

from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper

class test_CodeBuild_Jupyter(Test_Helper):
    def setUp(self):
        super().setUp()
        self.result = None
        self.build_id = 'OSBot-Jupyter:baea0626-3ad2-4e47-a41e-ff82ce5865ad'
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



class test_CodeBuild_Build_Errors(TestCase):
    def setUp(self):
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # Debug errors
    def test__list_build_ids(self):
        code_build = CodeBuild(None,None)
        self.last_10_builds = list(code_build.project_builds_ids('OSBot-Jupyter'))[0:10]
        print()
        for build_id in self.last_10_builds:
            build_info = code_build.build_info(build_id)
            print(build_id,build_info.get('buildStatus'))

            #
            # if 'STOPPED' == build_info.get('buildStatus'):

            #     jp_code_build = CodeBuild_Jupyter(build_id)
            #     messages = jp_code_build.build_log_messages()
            #     print(' '.join(messages))
            #     break

    def test__find_detect_build_that_fails_to_build(self):
        build_id = 'OSBot-Jupyter:6581a0da-1f88-4346-874f-6b80ab071cf9'
        jp_code_build = CodeBuild_Jupyter(build_id)
        messages = jp_code_build.build_log_messages()
        print(' '.join(messages))