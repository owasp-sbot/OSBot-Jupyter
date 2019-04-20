from time                                import sleep
from unittest                            import TestCase
from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build


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
