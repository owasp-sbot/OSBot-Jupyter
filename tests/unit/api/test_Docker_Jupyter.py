from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Docker_Jupyter import Docker_Jupyter, Docker


class test_Docker(TestCase):
    def setUp(self):
        self.docker = Docker()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_containers(self):
        self.result = dir(self.docker.containers()[0])


    def test_images(self):
        assert len(self.docker.images()) > 10


class test_Docker_Jupyter(TestCase):

    def setUp(self):
        self.image_name = 'local/jupyter:latest'
        self.image_name = '244560807427.dkr.ecr.eu-west-2.amazonaws.com/osbot-jupyter:latest'
        self.docker_jp  = Docker_Jupyter(self.image_name)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_container(self):
        self.result = self.docker_jp.container()

    def test_logs(self):
        print(self.docker_jp.logs())
        #self.result = first.logs().decode()

    def test_running(self):
        self.result = self.docker_jp.running()

    # def test_stop_start(self):
    #     self.docker_jp.stop()
    #     self.docker_jp.start()
    #     self.result = self.docker_jp.logs()

    def test_token(self):
        self.result = self.docker_jp.token()

    def test_url(self):
        self.result = self.docker_jp.url()