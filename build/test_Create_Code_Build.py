from time                                import sleep
from unittest                            import TestCase
from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Dev import Dev


class test_Create_Code_Build(TestCase):

    def setUp(self):
        self.project_name    = 'OSBot-Jupyter'
        self.account_id      = IAM().account_id()
        self.api             = Create_Code_Build(account_id=self.account_id, project_name=self.project_name)

    def create_project_with_container__jupyter(self):
        kvargs = {
            'name'        : self.api.project_name,
            'source'      : { 'type'                   : 'GITHUB',
                           'location'                  : self.api.project_repo                 },
            'artifacts'   : {'type'                    : 'NO_ARTIFACTS'                    },
            'environment' : {'type'                    : 'LINUX_CONTAINER'                  ,
                            'image'                    : 'jupyter/base-notebook'            ,
                            'computeType'              : 'BUILD_GENERAL1_LARGE'            },
            'serviceRole' : self.api.service_role
        }
        return self.api.code_build.codebuild.create_project(**kvargs)


    def test_create_code_build_and_trigger_first_build(self):
        #policies = self.api.policies__with_ecr_and_3_secrets()
        #self.api.create_role_and_policies(policies)
        #sleep(15)                                                        # to give time for AWS to sync up internally
        self.create_project_with_container__jupyter()
        self.api.code_build.build_start()

    def test_get_task_details(self):
        #build_id ='OSBot-Jupyter:741451df-d586-4f08-bdb5-5eff6d14d04a'
        #result = self.api.code_build.build_info(build_id)
        def find_starts(array, text):
            return [item for item in array if item.startswith('t=')]

        def find_in(array, text):
            return [item for item in array if text in item]




        from osbot_aws.apis.Logs import Logs
        logs = Logs(group_name = '/aws/codebuild/OSBot-Jupyter' , stream_name = '741451df-d586-4f08-bdb5-5eff6d14d04a')

        messages= logs.messages()
        ngrok_messages = find_starts(messages,'t=')
        ngrok_url      = find_in(messages, 'name=command_line addr')[0].split('url=')[1].strip()
        jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()

        Dev.pprint(ngrok_url,jupyter_token)
        #for line in ngrok_messages:
        #    print(line)

