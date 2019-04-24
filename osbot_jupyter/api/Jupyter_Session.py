from osbot_jupyter.api.Jupyter_API import Jupyter_API


class Jupyter_Session(Jupyter_API):

    def __init__(self, server=None, token=None, session_id=None):
        self.session_id = session_id
        super().__init__(server,token)

    def sessions(self):
        items = {}
        for session in self.http_get('sessions'):
            items[session.get('id')] = session
        return items

    def sessions_ids(self):
        return list(set(self.sessions()))

    def set_session_id(self,value):
        self.session_id = value
        return self

