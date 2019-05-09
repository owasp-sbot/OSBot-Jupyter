from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper


class Jupyter_Commands:

    @staticmethod
    def get_active_builds(*params):
        return "{0}".format(list(CodeBuild_Jupyter_Helper().get_active_builds().keys()))

    @staticmethod
    def stop_all_active(*params):
        return CodeBuild_Jupyter_Helper().stop_all_active()

    @staticmethod
    def get_active_server(*params):
        slack_message("[get_active_server] {0}".format(params))
        server, token = CodeBuild_Jupyter_Helper().get_active_server_details()
        return "{0}?token={1}".format(server, token)