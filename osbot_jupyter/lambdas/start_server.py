from osbot_aws.helpers.Lambda_Helpers import slack_message

def run(event, context):
    try:
        repo_name   = event.get('repo_name')
        channel     = event.get('channel')
        team_id     = event.get('team_id')
        user        = event.get('user')
        server_size = event.get('server_size','small')

        slack_message(f":point_right: Hi <@{user}>, starting Jupyter server for you with the repo `{repo_name}` with server size `{server_size}`.\n :information_source: This should take between 60 and 150 seconds", [], channel, team_id)

        from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
        login_url = CodeBuild_Jupyter_Helper().start_build_for_repo_and_wait_for_jupyter_load(repo_name=repo_name,user=user,server_size=server_size)
        if login_url:
            slack_message(":point_right: Server started ok, please use this link to open it:\n {0}".format(login_url), [], channel, team_id)
        else:
            slack_message(":red_circle: Could not find server (or it took too long to start). Please check that the repo `{0}` exists.".format(repo_name),[], channel, team_id)

    except Exception as error:
        slack_message(f":red_circle: Something went wrong when starting the {repo_name} Jupyter notebook: {0}".format(error),[], channel, team_id)
        return "{0}".format(error)

