from osbot_jupyter.api.CodeBuild_Jupyter        import CodeBuild_Jupyter
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from osbot_jupyter.api.Jupyter_API              import Jupyter_API
from osbot_jupyter.api.Jupyter_Web              import Jupyter_Web


class Live_Notebook:
    def __init__(self, short_id=None, headless=True):
        self.headless            = headless
        self.short_id            = None
        self.build_id            = None
        self._code_build_Jupyter = None
        self._jupyter_web        = None
        self._jupyter_api        = None
        self._needs_login        = True
        self.jupyter_helper      = CodeBuild_Jupyter_Helper()
        if short_id:
            self.set_build_from_short_id(short_id)

    # config methods
    def set_build_id(self,build_id):
        self.build_id = build_id
        return self

    def set_build_from_short_id(self, short_id):
        for build_id in self.jupyter_helper.get_active_builds():
            if short_id in build_id:
                self.build_id = build_id
                self.short_id = short_id
                return self
        return None

    def code_build_Jupyter(self):
        if self._code_build_Jupyter is None and self.build_id:
            self._code_build_Jupyter = CodeBuild_Jupyter(self.build_id)
        return self._code_build_Jupyter

    def jupyter_web(self):
        if self._jupyter_web is None:
            server, token = self.code_build_Jupyter().get_server_details_from_logs()
            self._jupyter_web = Jupyter_Web(server=server, token=token,headless=self.headless)
        return self._jupyter_web

    def jupyter_api(self):
        if self._jupyter_api is None:
            server, token = self.code_build_Jupyter().get_server_details_from_logs()
            self._jupyter_api = Jupyter_API(server=server, token=token)
        return self._jupyter_api

    # api Methods

    def contents(self,path=''):
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


    def screenshot(self,path, width=None):
        return (self.login            ()
                    .open             (path)
                    .browser_width    (width)
                    .screenshot_base64())

    def login(self):
        if self._needs_login is True:
            self.jupyter_web().login()
            self._needs_login = False
        return self.jupyter_web()

    def stop(self):
        return self.code_build_Jupyter().code_build.codebuild.stop_build(id=self.build_id).get('build')





