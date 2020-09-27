from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_jupyter.api.Live_Notebook           import Live_Notebook
from osbot_utils.utils import Misc


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
        Lambda('gw_bot.lambdas.png_to_slack').invoke({'png_data': png_data, 'team_id': team_id, 'channel': channel})

class Jupyter_Web_Commands:

    api_version = 'v0.40 (GW Bot)'

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
        if file_type == 'notebook':
            result = jupyter_api.notebook_create(file_path, file_contents)
        else:
            result = jupyter_api.file_create(file_path, file_contents)
        if result.get('status') == 'ok':
            if file_type == 'notebook':
                url = "{0}/notebooks/{1}".format(jupyter_api.server, file_path)
            else:
                url = "{0}/edit/{1}".format(jupyter_api.server, file_path)
            return send_message(':white_check_mark:  `{0}` created ok, you can see it here: {1}'.format(file_type, url),channel, team_id)
        else:
            return send_message(':red_circle: Error creating notebook ```{0}```'.format(result.get('data')),channel, team_id)

    @staticmethod
    def exec(team_id=None, channel=None, params=None):
        try:
            event = Misc.array_pop(params)  # original slack event object

            if not params or len(params) < 2:
                return send_message(':red_circle: You must provide the following params: `Server Id` and `code` (to execute)',channel, team_id)

            short_id   = str(Misc.array_pop(params, 0))
            code       = ' '.join(params).replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'")
            notebook   = Live_Notebook()

            if notebook.set_build_from_short_id(short_id) is None:
                return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id)

            (target_notebook,created) = notebook.get_python_invoke_file()
            if created:
                send_message(':point_right: Created temp file for dynamic execution: `{0}`'.format(target_notebook),channel, team_id)

            send_message(':point_right: Running code with size `{0}` on server `{1}` (on file `{2}`)'.format(len(code), short_id, target_notebook), channel, team_id)

            result = notebook.execute_python_in_notebook(target_notebook, code, event)

            if channel:
                return send_message(':point_right: Code executed, here is the output:\n ```{0}```'.format(result),channel,team_id)
            else:
                return result
        except Exception as error:
            return send_message(':red_circle: Error: {0}'.format(error),channel, team_id)

    @staticmethod
    def view_exec_file(team_id=None, channel=None, params=None):
        #event = Misc.array_pop(params)  # original slack event object
        if not params or len(params) < 2:
            build_id = 'gscs'               # for now default to this one
            #return send_message(':red_circle: You must provide the following params: `Server Id`', channel, team_id)
        else:
            build_id = str(Misc.array_pop(params, 0))

        notebook = Live_Notebook()
        if notebook.set_build_from_short_id(build_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(build_id)


        (target_notebook, created) = notebook.get_python_invoke_file()
        send_message(":point_right: Today's python execution file in server `{0}` is `{1}`, here is what it looks like:".format(build_id, target_notebook), channel, team_id)
        width  = 1200
        height = 1200
        delay  = 2
        png_data = notebook.screenshot(path=target_notebook, width=width, height=height, delay=delay, apply_ui_fixes=False)

        return send_png_to_slack(png_data, channel,team_id)

    @staticmethod
    def screenshot(team_id=None, channel=None, params=None ,headless=True):
        event = Misc.array_pop(params)  # original slack event object (don't think this is needed anymore)
        if not params or len(params) == 0:
            return send_message(':red_circle: You must provide an Server Id. Please use `jupyter servers` to see the current list of live servers',channel,team_id)

        from osbot_jupyter.api.Live_Notebook import Live_Notebook

        short_id = Misc.array_pop(params, 0)
        path     = Misc.array_pop(params, 0)
        width    = Misc.to_int(Misc.array_pop(params, 0))
        height   = Misc.to_int(Misc.array_pop(params, 0))
        delay    = Misc.to_int(Misc.array_pop(params, 0))

        if not path  : path = '/'
        if not width : width = 1200
        if not height: height = 500
        if delay is None: delay = 1                             # add one second delay if no value is provided

        notebook = Live_Notebook(headless=headless)

        if notebook.set_build_from_short_id(short_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id)

        send_message(':point_right: taking screenshot of `{0}` with width `{1}`, (min) height `{2}` and delay `{3}`'.format(path, width,height,delay), channel,team_id)

        png_data = notebook.screenshot(path=path, width=width, height=height, delay=delay, apply_ui_fixes=False) # when calling the sceenshot via the web command,  don't apply the UI fixes

        return send_png_to_slack(png_data, channel,team_id)

    @staticmethod
    def preview(team_id=None, channel=None, params=None , headless=True):
        event = Misc.array_pop(params)  # original slack event object

        if not params or len(params) < 2:
            return send_message(':red_circle: You must provide an Server Id and file to process. Please use `jupyter servers` to see the current list of live servers',channel,team_id)


        short_id = Misc.array_pop(params, 0)
        path     = Misc.array_pop(params, 0)
        width    = Misc.to_int(Misc.array_pop(params, 0, 1200))
        height   = Misc.to_int(Misc.array_pop(params, 0, 800 ))
        delay    = Misc.to_int(Misc.array_pop(params, 0, 0))

        if width  is None: width  = 1200
        if height is None: height = 800
        if delay  is None: delay  = 0


        notebook = Live_Notebook(headless=headless)

        if notebook.set_build_from_short_id(short_id) is None:
            return ':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id)

        if '?show-code' in path:
            path = f'nbconvert/html/{path}'
        else:
            path = f'nbconvert/html/{path}?download=false&osbot-no-code'

        send_message(':point_right: taking screenshot of `{0}` with width `{1}`, (min) height `{2}` and delay `{3}`'.format(path, width,height,delay), channel,team_id)

        png_data = notebook.screenshot(path=path, width=width, height=height, delay=delay, apply_ui_fixes=True)

        return send_png_to_slack(png_data, channel,team_id)

    # @staticmethod
    # def report(team_id=None, channel=None, params=None):
    #     event  = Misc.array_pop(params)  # original slack event object
    #     name   = Misc.array_pop(params)
    #     report = "reports/{0}.ipynb".format(name)
    #     params = ['gscs',report, event]
    #     return Jupyter_Web_Commands.preview(team_id, channel, params)

    @staticmethod
    def update_notebook(team_id=None, channel=None, params=None):
        event = Misc.array_pop(params)  # original slack event object

        if not params or len(params) < 2:
            return send_message(':red_circle: You must provide the following params: `Server Id` and `notebook path` (to update)', channel,team_id)

        short_id        = str(Misc.array_pop(params, 0))
        target_notebook = Misc.array_pop(params, 0)

        if '.ipynb' not in target_notebook:
            target_notebook += '.ipynb'

        notebook = Live_Notebook()
        if notebook.set_build_from_short_id(short_id) is None:
            return send_message(':red_circle: Could not find Jupyter server with id `{0}`. Please use `jupyter servers` to see the current list of live servers'.format(short_id), channel, team_id)

        if notebook.jupyter_api().contents(target_notebook) is None:
            return send_message(":red_circle: Could not find notebook `{0}` in server `{1}`".format(target_notebook, short_id),channel, team_id)


        send_message(":point_right: Updating notebook `{0}` on server `{1}`".format(target_notebook,short_id), channel, team_id)

        target_notebook_fixed = "notebooks/{0}".format(target_notebook)
        code = '!cd ../../..; jupyter nbconvert --to notebook --inplace --execute {0}'.format(target_notebook_fixed)

        #note for longer executions the save is not working ok
        (invoke_notebook, created) = notebook.get_python_invoke_file()
        send_message(':point_right: Running code with size `{0}` on server `{1}` (on file `{2}`)'.format(len(code), short_id, invoke_notebook), channel, team_id)

        result = notebook.execute_python_in_notebook(invoke_notebook,code, event)

        #send_message("result: ```{0}``` ".format(result),channel, team_id)

        if result and ('[NbConvertApp] Writing' not in result): #or ('[js eval error]' in result):
            if 'matched no files' in result:
                send_message(":red_circle:  Update failed, could not find notebook \n ```{0}```".format(target_notebook_fixed), channel, team_id)
                send_message("Here is the execution code: ```{0}````".format(code), channel, team_id)
                return
            else:
                return send_message(":red_circle:  Update failed: \n ```{0}```".format(result), channel, team_id)

        send_message(":point_right: Notebook updated ok", channel, team_id) # need to double check
        params = [short_id, target_notebook, event]
        return Jupyter_Web_Commands.preview(team_id,channel,params)

    @staticmethod
    def version(team_id=None, channel=None, params=None):
        return Jupyter_Web_Commands.api_version

    # with business logic

    @staticmethod
    def milestone(team_id=None, channel=None, params=None):
        Misc.array_pop(params)                                  # original slack event object

        if not params or len(params) < 2:
            return send_message(':red_circle: You must provide the following params: `Server Id` and `jira ID`',channel, team_id)

        short_id = str(Misc.array_pop(params, 0))
        source   = str(Misc.array_pop(params, 0)).upper()

        source_notebook = "icap/gwbot-reporting/TEST-milestones-TEST.ipynb"
        target_notebook = f"icap/gwbot-reporting/{source}.ipynb"

        send_message(f":python: creating milestone view for {source}", channel, team_id)  # need to double check

        exec_params    = [short_id, f"!papermill ../../{source_notebook} ../../{target_notebook} -p source {source}", {} ]
        preview_params = [short_id, f"{target_notebook}"                                                            , {} ]

        Jupyter_Web_Commands.exec   (channel=channel, params=exec_params   )
        Jupyter_Web_Commands.preview(channel=channel, params=preview_params)
