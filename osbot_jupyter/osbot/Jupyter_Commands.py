from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper


def send_message(message, channel, team_id):
    if channel:
        slack_message(message, [], channel, team_id)
    else:
        print(message)

class Jupyter_Commands:         #*params = (team_id=None, channel=None, params=None)

    @staticmethod
    def get_active_builds(*params):
        return "{0}".format(list(CodeBuild_Jupyter_Helper().get_active_builds().keys()))

    @staticmethod
    def servers(team_id=None, channel=None, params=None):
        text         = ":point_right: Here are the running servers:"
        servers_text = ""
        attachments = []
        for build_id,build in CodeBuild_Jupyter_Helper().get_active_builds().items():
            #print(build_id)
            build_info = build.build_info()
            Dev.pprint(build_info)
            variables = {}
            for variable in build_info.get('environment').get('environmentVariables'):
                variables[variable.get('name')] = variable.get('value')

            repo_name  = variables.get('repo_name')
            user       = variables.get('user')
            timeout    = build_info.get('timeoutInMinutes')
            small_id   = build_id[-5:]
            server_url = build.url()

            if server_url is None:
                user_text = "(server booting up)"
            else:
                user_text = "<{0}|open>".format(server_url)
            #    servers_text += "*{0}*: booting up\n".format(repo_name, server_url)
            #else:
            time = "{0}".format(build_info.get('startTime').strftime("%H:%M"))
            servers_text += "*{1}*: {2} (id: `{0}`, user: <@{3}>, started: {4}, timeout: {5})\n".format(
                                small_id, repo_name,user_text,user,time, timeout)

        attachments.append({"text":servers_text, 'color': 'good'})

        slack_message(text, attachments, channel, team_id)


        #return "{0}".format(list(CodeBuild_Jupyter_Helper().get_active_builds().keys()))

    @staticmethod
    def start_server(team_id=None, channel=None, params=None):
        event     = Misc.array_pop(params)
        user      = Misc.get_value(event,'data', {}).get('user')
        repo_name = Misc.array_pop(params,0)

        if repo_name is None:
            return ":red_circle: you need to provide an git repo with notebooks, for example try `gs-notebook-gscs`"

        payload = {'repo_name': repo_name, "channel": channel, "team_id": team_id, 'user':user}
        Lambda('osbot_jupyter.lambdas.start_server').invoke_async(payload)


    @staticmethod
    def stop_all(*params):
        return CodeBuild_Jupyter_Helper().stop_all_active()

    @staticmethod
    def get_active_server(*params):
        slack_message("[get_active_server] {0}".format(params))
        server, token = CodeBuild_Jupyter_Helper().get_active_server_details()
        return "{0}?token={1}".format(server, token)