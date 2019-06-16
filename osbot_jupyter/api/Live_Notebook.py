import datetime

from osbot_jupyter.api.CodeBuild_Jupyter        import CodeBuild_Jupyter
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from osbot_jupyter.api.Jupyter_API              import Jupyter_API
from osbot_jupyter.api.Jupyter_Web              import Jupyter_Web
from osbot_jupyter.api.Jupyter_Web_Cell         import Jupyter_Web_Cell


class Live_Notebook:
    def __init__(self, short_id=None, headless=True):
        self.headless            = headless
        self.short_id            = None
        self.build_id            = None
        self._browser            = None
        self._code_build_Jupyter = None
        self._jupyter_cell       = None
        self._jupyter_web        = None
        self._jupyter_api        = None
        self._server_details     = None
        self._needs_login        = True
        self.jupyter_helper      = CodeBuild_Jupyter_Helper()
        self.execute_python_file = 'notebooks/setup/gsbot-invoke.ipynb'
        if short_id:
            self.set_build_from_short_id(short_id)

    # global objects
    def browser(self):      # we have make sure there is only one instance of browser created
        if self._browser is None:
            from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
            browser_helper = Browser_Lamdba_Helper(headless=self.headless).setup()
            self._browser = browser_helper.api_browser
        return self._browser

    def jupyter_cell(self):
        if self._jupyter_cell is None:
            server, token = self.server_details()
            self._jupyter_cell = Jupyter_Web_Cell(server=server, token=token, headless=self.headless, browser= self.browser())
        return self._jupyter_cell

    def jupyter_web(self):
        if self._jupyter_web is None:
            server, token = self.server_details()
            self._jupyter_web = Jupyter_Web(server=server, token=token,headless=self.headless, browser= self.browser())
        return self._jupyter_web

    def jupyter_api(self):
        if self._jupyter_api is None:
            server, token = self.server_details()
            self._jupyter_api = Jupyter_API(server=server, token=token)
        return self._jupyter_api


    # config methods
    def set_build_id(self,build_id):
        self.build_id = build_id
        return self

    def set_build_from_short_id(self, short_id):
        if short_id and type(short_id) is str:
            active_builds = self.jupyter_helper.get_active_builds()
            if active_builds:
                for build_id in active_builds:
                    if short_id in build_id:
                        self.build_id = build_id
                        self.short_id = short_id
                        return self
        return None

    def code_build_Jupyter(self):
        if self._code_build_Jupyter is None and self.build_id:
            self._code_build_Jupyter = CodeBuild_Jupyter(self.build_id)
        return self._code_build_Jupyter

    # # NOT WORKING IN LAMBDA (I think it is because the Javascript is not being executed ok)
    # def execute_python(self, python_code,keep_contents=True, target=None):
    #     jp_web  = self.jupyter_web()
    #     jp_cell = self.jupyter_cell()           # the prob is the browser object is being created twice
    #     if target is None:
    #         target = self.execute_python_file
    #     if (target in jp_web.url()) is False:
    #         jp_web.open(target)
    #     if not keep_contents:
    #         jp_cell.clear()
    #     jp_cell.execute(python_code)
    #     #jp_cell.new()
    #     #jp_cell.text('some content')
    #     return jp_cell.output_wait_for_data()

    def server_details(self):
        if self._server_details is None:
            if self.code_build_Jupyter():
                self._server_details = self.code_build_Jupyter().get_server_details_from_logs()
        return self._server_details

    # api Methods

    def files(self,path=''):
        text_body = ""
        data       = self.jupyter_api().contents(path)
        if data is None:
            text_title = ":red_circle: Folder `{0}` not found in server `{1}`".format(path, self.short_id)
        else:
            if path == '' : path='/'
            files   = []
            folders = []
            text_title = ":point_right: Here are the files and folders for `{0}` in the server `{1}`".format(path, data.get('type'),self.short_id)
            for item in data.get('content'):
                url         = "{0}/tree/{1}".format(self.jupyter_api().server, item.get('path'))
                url_preview = "{0}/{1}".format(self.jupyter_web().server, self.jupyter_web().resolve_url_notebook_preview(item.get('path')))
                if item.get('type') == 'directory':
                    #folders.append("<{0}|{1}> (<{2}|preview>)".format(url,item.get('name'), url_preview))
                    folders.append("<{0}|{1}>".format(url,item.get('name')))
                else:
                    files.append(" - {0} (<{1}|edit> , <{2}|preview>)\n".format(item.get('name'), url, url_preview))
                    #files.append("<{0}|{1}>".format(url,item.get('name')))

            if files:
                text_body += '*Files:* \n{0}\n\n'.format(''.join(files))
            if folders:
                text_body += '*Folders:* {0}'.format(' , '.join(folders))

        return text_title, text_body


    def screenshot(self,path=None, width=None,height=None, delay=None, apply_ui_fixes=True):
        jupyter_web = self.login()
        (
            jupyter_web.open         (path)
                       .browser_size (width,height)
                       .wait_seconds (delay)
        )
        if apply_ui_fixes:
            jupyter_web.ui_css_fixes(width)

        if path and 'osbot-no-code' in path:
            jupyter_web.ui_hide_input_boxes()

        return jupyter_web.screenshot_base64()

    def login(self):
        if self._needs_login is True:
            self.jupyter_web().login()
            self._needs_login = False
        return self.jupyter_web()

    def stop(self):
        return self.code_build_Jupyter().code_build.codebuild.stop_build(id=self.build_id).get('build')

    def execute_python_in_notebook(self, target_notebook, code, source_event):
        self.login()
        self.jupyter_web().open(target_notebook)

        self.jupyter_cell().wait_seconds(1)  # refactor with better method

        self.jupyter_cell().new_top()                                                              \
                           .to_markdown()                                                          \
                           .text("### Code above requested by: \n ```{0}```".format(source_event)) \
                           .execute()
        result = self.jupyter_cell().execute_python(code).output_wait_for_data()

        self.jupyter_cell().save_notebook()
        return result

    def get_python_invoke_file(self):
        today           = '{0}'.format(datetime.date.today().strftime('%d-%b-%y'))
        target_notebook = 'users/gsbot/invoke-{0}.ipynb'.format(today)
        created         = False
        if self.jupyter_api().contents(target_notebook) is None:  # we need to create the file
            self.jupyter_api().notebook_create(target_notebook)
            created = True
        target_notebook = "notebooks/{0}".format(target_notebook)

        return target_notebook, created