import datetime

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.Live_Notebook import Live_Notebook


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
        send_message(":point_right: got screenshot with size `{0}` (sending it to slack) ".format(len(png_data)), channel, team_id)
        Lambda('utils.png_to_slack').invoke({'png_data': png_data, 'team_id': team_id, 'channel': channel})

class Jupyter_Web_Commands:

    @staticmethod
    def create_file(team_id=None, channel=None, params=None):
        event = Misc.array_pop(params)          # original slack event object
        if not params or len(params) <2:
            return send_message(':red_circle: You must provide the following params: `Server Id` and `notebook path`',channel,team_id)

        build_id      = str(Misc.array_pop(params, 0))
        file_path     = Misc.array_pop(params, 0)
        file_contents = ' '.join(params)
        notebook      = Live_Notebook()

        file_type     = 'notebook' if '.ipynb' in file_path else 'file'

        if notebook.set_build_from_short_id(build_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(build_id)

        send_message(':point_right: Creating `{0}` on server `{1}` at location `{2}` with content of size `{3}`'.format(file_type, build_id, file_path, len(file_contents)), channel, team_id)

        jupyter_api = notebook.jupyter_api()
        if file_type is 'notebook':
            result = jupyter_api.notebook_create(file_path, file_contents)
        else:
            result = jupyter_api.file_create(file_path, file_contents)
        if result.get('status') == 'ok':
            if file_type is 'notebook':
                url = "{0}/notebooks/{1}".format(jupyter_api.server, file_path)
            else:
                url = "{0}/edit/{1}".format(jupyter_api.server, file_path)
            return send_message(':white_check_mark:  `{0}` created ok, you can see it here: {1}'.format(file_type, url),channel, team_id)
        else:
            return send_message(':red_circle: Error creating notebook ```{0}```'.format(result.get('data')),channel, team_id)

    @staticmethod
    def execute_python(team_id=None, channel=None, params=None):
        try:
            event = Misc.array_pop(params)  # original slack event object
            if not params or len(params) < 2:
                return send_message(':red_circle: You must provide the following params: `Server Id` and `code` (to execute)',channel, team_id)

            build_id   = str(Misc.array_pop(params, 0))
            code       = ' '.join(params).replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'")
            notebook   = Live_Notebook()

            if notebook.set_build_from_short_id(build_id) is None:
                return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(build_id)

            (target_notebook,created) = notebook.get_python_invoke_file()
            if created:
                send_message(':point_right: Created temp file for dynamic execution: `{0}`'.format(target_notebook),channel, team_id)

            send_message(':point_right: Running code with size `{0}` on server `{1}` (on file `{2}`)'.format(len(code), build_id, target_notebook), channel, team_id)

            result = notebook.execute_python_in_notebook(target_notebook, code, event)

            if channel:
                return send_message(':point_right: Code executed, here is the output:\n ```{0}```'.format(result),channel,team_id)
            else:
                return result
        except Exception as error:
            return send_message(':red_circle: Error: {0}'.format(error),channel, team_id)

    @staticmethod
    def show_python_invoke_file(team_id=None, channel=None, params=None):
        #event = Misc.array_pop(params)  # original slack event object
        if not params or len(params) < 2:
            return send_message(':red_circle: You must provide the following params: `Server Id`', channel, team_id)

        build_id = str(Misc.array_pop(params, 0))
        notebook = Live_Notebook()
        if notebook.set_build_from_short_id(build_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(build_id)


        (target_notebook, created) = notebook.get_python_invoke_file()
        send_message(":point_right: Today's python execution file is: `{0}`, here is what it looks like".format(target_notebook), channel, team_id)
        width  = 1200
        height = 1200
        delay  = 2
        png_data = notebook.screenshot(path=target_notebook, width=width, height=height, delay=delay, apply_ui_fixes=False)

        return send_png_to_slack(png_data, channel,team_id)

    @staticmethod
    def screenshot(team_id=None, channel=None, params=None):
        event = Misc.array_pop(params)  # original slack event object
        if not params or len(params) == 0:
            return send_message(':red_circle: You must provide an Server Id. Please use `jupyter servers` to see the current list of live servers',channel,team_id)

        from osbot_jupyter.api.Live_Notebook import Live_Notebook

        short_id = Misc.array_pop(params, 0)
        path     = Misc.array_pop(params, 0)
        width    = Misc.to_int(Misc.array_pop(params, 0))
        height   = Misc.to_int(Misc.array_pop(params, 0))
        delay    = Misc.to_int(Misc.array_pop(params, 0))

        if delay is None: delay = 1                             # add one second delay if no value is provided

        notebook = Live_Notebook()

        if notebook.set_build_from_short_id(short_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id)

        send_message(':point_right: taking screenshot of `{0}` with width `{1}`, height `{2}` and delay `{3}`'.format(path, width,height,delay), channel,team_id)

        png_data = notebook.screenshot(path=path, width=width, height=height, delay=delay, apply_ui_fixes=False) # when calling the sceenshot via the web command,  don't apply the UI fixes

        return send_png_to_slack(png_data, channel,team_id)