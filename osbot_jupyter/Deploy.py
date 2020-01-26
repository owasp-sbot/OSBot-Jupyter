from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files


class Deploy:

    def __init__(self, lambda_name):
        self.package         = Lambda_Package(lambda_name)
        self.tmp_s3_bucket = 'gs-lambda-tests'
        self.tmp_s3_key    = 'gsbot/{0}.zip'.format(lambda_name)
        self.setup()

    def setup(self):
        (self.package._lambda.set_s3_bucket(self.tmp_s3_bucket)
                             .set_s3_key   (self.tmp_s3_key)
                             .set_xrays_on())


    def deploy(self, delete_before=False):
        if delete_before:
            self.package.delete()
        self.package.update_code()

    def deploy_screenshot(self):
        self.package.add_module('osbot_browser')
        self.package.update_code()

    def deploy_jupyter_web(self):
        self.package.add_module('osbot_browser')
        self.package.update_code()
