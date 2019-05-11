from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter
from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper
from osbot_jupyter.api.Jupyter_Web import Jupyter_Web


class Live_Notebook:
    def __init__(self, headless=True):
        self.headless            = headless
        self.build_id            = None
        self._code_build_Jupyter = None
        self._jupyter_web        = None
        self._needs_login        = True
        self.jupyter_helper      = CodeBuild_Jupyter_Helper()

    # config methods
    def set_build_id(self,build_id):
        self.build_id = build_id
        return self

    def set_build_from_short_id(self, short_id):
        for build_id in self.jupyter_helper.get_active_builds():
            if short_id in build_id:
                self.build_id = build_id
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

    # api Methods

    def screenshot(self,path, width=None):
        return (self.login            ()
                    .open_notebook    (path)
                    .browser_width    (width)
                    .screenshot_base64())

    def login(self):
        if self._needs_login is True:
            self.jupyter_web().login()
            self._needs_login = False
        return self.jupyter_web()

    def stop(self):
        return self.code_build_Jupyter().code_build.codebuild.stop_build(id=self.build_id).get('build')





