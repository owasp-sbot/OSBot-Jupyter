from osbot_jupyter.api.Jupyter_API import Jupyter_API


class Jupyter_Kernel(Jupyter_API):

    def __init__(self, server=None, token=None, kernel_id=None):
        self.kernel_id = kernel_id
        super().__init__(server,token)

    def list(self):
        return self.http_get('kernels')
        items = {}
        for session in self.http_get('kernels'):
            items[session.get('id')] = session
        return items