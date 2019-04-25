import json
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_Kernel(TestCase):

    kernel_id = None
    server    = None

    @classmethod
    def setUpClass(cls):
        server                        = Test_Server().docker()
        test_Jupyter_Kernel.server    = server
        test_Jupyter_Kernel.kernel_id = server.jupyter_kernel().new().kernel_id

    @classmethod
    def tearDownClass(cls):
        kernel_id   = test_Jupyter_Kernel.kernel_id
        server      = Test_Server().docker()
        jp_kernel   = server.jupyter_kernel().set_kernel_id(kernel_id)
        jp_kernel.delete()
        assert jp_kernel.exists() is False

    def setUp(self):
        kernel_id = test_Jupyter_Kernel.kernel_id
        server = Test_Server().docker()
        self.jp_kernel  = server.jupyter_kernel().set_kernel_id(kernel_id)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_delete__new(self):
        assert self.jp_kernel.delete() is True
        assert self.jp_kernel.delete() is False
        assert self.jp_kernel.new()    == self.jp_kernel
        assert self.jp_kernel.exists()  is True

    def test_delete_all(self):
        before = len(self.jp_kernel.kernels())
        after  = len(self.jp_kernel.delete_all())
        assert after == before
        assert after  > 0
        assert len(self.jp_kernel.kernels()) == 0
        assert self.jp_kernel.kernel_id      is None
        assert self.jp_kernel.new()          is self.jp_kernel
        assert len(self.jp_kernel.kernels()) == 1
        test_Jupyter_Kernel.kernel_id = self.jp_kernel.kernel_id


    def test_exists(self):
        assert self.jp_kernel.exists()

    def test_info(self):
        info = self.jp_kernel.info()
        assert set(info)        == {'last_activity', 'connections', 'name', 'id', 'execution_state'}
        assert info.get('name') == 'python3'
        assert info.get('id')   == self.jp_kernel.kernel_id

    def test_kernels(self):
        assert len(self.jp_kernel.kernels()) > 0
        self.result = self.jp_kernel.kernels()

    def test_kernels_ids(self):
        assert len(self.jp_kernel.kernels_ids()) > 0

        #self.result = self.jp_kernel.kernels()

    def test_execute_get_connection(self):
        ip   = 'localhost'
        port = 8888
        ws = self.jp_kernel.execute_get_connection(ip, port)
        assert type(ws).__name__ == 'WebSocket'
        assert ws.connected == True
        assert ws.status    == 101
        assert ws.headers.get('connection') == 'Upgrade'
        assert ws.headers.get('server'    ) == 'TornadoServer/6.0.2'
        assert ws.headers.get('upgrade'   ) == 'websocket'
        ws.close()


    # the `execute` is not as reliable as I would expected it to be
    # this tests proves that there are times when the execution result is missed
    def test_execute(self):
        result = {}
        for i in range(1,10):
            response = json.dumps(self.jp_kernel.execute("40+2"))
            if result.get(response) is None: result[response] = 0
            result[response] += 1
        assert '{"output": "42", "input": "40+2", "status": "ok"}' in list(set(result))
        assert '{"output": null, "input": "40+2", "status": "ok"}' in list(set(result))
        return
        #assert self.jp_kernel.execute("40+2") == {'input': '40+2', 'output': '42', 'status': 'ok'}

        #code = "a = 42; a"
        #code = "a = {'answer': 42}; from time import sleep; sleep(1); 'aaa'.encode()"
#         code = """
# import requests
# html = requests.get('https://www.google.com/aaaa').status_code
# html
# """
        #messages = self.jp_kernel.execute(code)


