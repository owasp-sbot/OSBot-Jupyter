from time                                import sleep
from unittest                            import TestCase
from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy


class test_Create_Code_Build(TestCase):

    def setUp(self):
        Deploy().setup()
        self.project_name    = 'OSBot-Jupyter'
        self.account_id      = IAM().account_id()
        self.api             = Create_Code_Build(account_id=self.account_id, project_name=self.project_name)

    def create_project_with_container__osbot_jupyter(self):
        kvargs = {
            'name'        : self.api.project_name,
            'source'      : { 'type'                   : 'GITHUB',
                           'location'                  : self.api.project_repo                 },
            'artifacts'   : {'type'                    : 'NO_ARTIFACTS'                    },
            'environment' : {'type'                    : 'LINUX_CONTAINER'                  ,
                            'image'                    : '{0}.dkr.ecr.eu-west-2.amazonaws.com/osbot-jupyter:latest'.format(self.account_id)     ,
                            'computeType'              : 'BUILD_GENERAL1_SMALL'            ,
                            'imagePullCredentialsType' : 'SERVICE_ROLE'                    },
            'serviceRole' : self.api.service_role
        }
        return self.api.code_build.codebuild.create_project(**kvargs)

    def test_create_code_build_and_trigger_first_build(self):
        #policies = self.api.policies__with_ecr_and_3_secrets()
        #self.api.create_role_and_policies(policies)
        #sleep(15)                                                        # to give time for AWS to sync up internally
        #self.api.code_build.project_delete()
        self.create_project_with_container__osbot_jupyter()
        self.api.code_build.build_start()

    def test_get_task_details(self):
        from osbot_aws.apis.Logs import Logs


        def find_starts(array, text):
            return [item for item in array if item.startswith(text)]

        def find_in(array, text):
            return [item for item in array if text in item]

        #build_id = 'OSBot-Jupyter:a553dda5-953a-41b8-ae91-e068cba4f56b'

        result      = self.api.code_build.project_builds_ids(self.api.project_name)
        build_id    = result.__next__()        # get last one
        build_info  = self.api.code_build.build_info(build_id)
        group_name  = build_info.get('logs').get('groupName')
        stream_name = build_info.get('logs').get('streamName')
        #Dev.pprint(group_name,stream_name)
        logs        = Logs(group_name = group_name , stream_name = stream_name)

        messages= logs.messages()
        #ngrok_messages = find_starts(messages,'t=')
        ngrok_url      = find_in(messages, 'name=command_line addr')[0].split('url=')[1].strip()
        jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()

        Dev.pprint("{0}?token={1}".format(ngrok_url,jupyter_token))



