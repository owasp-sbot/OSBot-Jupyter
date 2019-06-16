from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


def run(event, context):
    try:

        channel = event.get('channel')
        team_id = event.get('team_id')
        params  = event.get('params')

        from osbot_jupyter.osbot.Jupyter_Web_Commands import Jupyter_Web_Commands

        result = Slack_Commands_Helper(Jupyter_Web_Commands).invoke(team_id, channel, params)
        if channel is None:
            return result

    except Exception as error:
        message = "[jupyter_web] Error: {0}".format(error)
        return message