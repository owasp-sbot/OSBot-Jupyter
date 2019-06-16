from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc


def send_message(message, channel, team_id):
    if channel:
        slack_message(message, [], channel, team_id)
    else:
        print(message)
        return message

def send_png_to_slack(png_data, channel, team_id):
    if channel is None:
        return png_data
    if len(png_data) == 3:
        send_message(":red_circle: error taking screenshot :{0} ".format(png_data), channel, team_id)
    else:
        send_message(":point_right: got screenshot with size `{0}` (sending it to slack) ".format(len(png_data)),
                     channel, team_id)
        Lambda('utils.png_to_slack').invoke_async({'png_data': png_data, 'team_id': team_id, 'channel': channel})

class Jupyter_Web_Commands:


    @staticmethod
    def screenshot(team_id=None, channel=None, params=None):
        if not params or len(params) == 0:
            return send_message(':red_circle: You must provide an Server Id. Please use `jupyter servers` to see the current list of live servers',channel,team_id)

        from osbot_aws.apis.Lambda import load_dependency
        load_dependency('requests')
        from osbot_jupyter.api.Live_Notebook import Live_Notebook

        short_id = Misc.array_pop(params, 0)
        path     = Misc.array_pop(params, 0)
        width    = Misc.to_int(Misc.array_pop(params, 0))
        height   = Misc.to_int(Misc.array_pop(params, 0))
        delay    = Misc.to_int(Misc.array_pop(params, 0))
        notebook = Live_Notebook()

        if notebook.set_build_from_short_id(short_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id)

        send_message(':point_right: taking screenshot of `{0}` with width `{1}`, height `{2}` and delay `{3}`'.format(path, width,height,delay), channel,team_id)
        png_data = notebook.screenshot(path=path, width=width, height=height, delay=delay)

        return send_png_to_slack(png_data, channel,team_id)