from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_jupyter.helpers.Test_Server import Test_Server


class test_Jupyter_API(TestCase):

    def setUp(self):
        self.notebook_name  = 'users/gsbot/gsbot-invoke.ipynb'
        #self.api           = Test_Server().docker().jupyter_api()
        self.api            = Test_Server().codebuild().jupyter_api()
        self.result         = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_version(self):
        assert self.api.version().get('version') == '5.7.8'

    # this is not working
    # def test_create(self):
    #     tmp_file = 'work/{0}.txt'.format(Misc.random_string_and_numbers())
    #     self.result = self.api.create(tmp_file)

    def test_contents(self):
        #self.api.files()
        self.api.contents('work')
        self.result = self.api.contents(self.notebook_name)

    def test_directory_contents(self):
        data = self.api.directory_contents('users/dinis')
        assert set(data) == {'files', 'folders'}
        assert len(data.get('files'  )) > 0
        assert len(data.get('folders')) > 0

    # # this won't work like this (too slow to get each folder contents
    # def test_directory_contents_recursive(self):
    #     from time import time
    #     start = time()
    #     self.api.directory_contents_recursive()
    #     duration = time() - start
    #     print('took {0:.2f} in unitest'.format(duration))

    def test_kernel_execute(self):
        self.result = self.api.kernel_code_execute('40+2')

    def test_kernels(self):
        self.result = self.api.kernels()

    def test_file_create(self):
        file_path    = 'users/gsbot/_created_by_test.txt'
        contents     = 'some text'
        new_notebook = self.api.file_create(file_path, contents)
        assert new_notebook.get('path') == file_path
        assert self.api.file_delete(file_path) is True

    def test_folder_create(self):
        folder_path    = 'users/gsbot/_an_temp_folder'
        new_folder = self.api.folder_create(folder_path)
        assert new_folder.get('path') == folder_path
        self.result = self.api.file_delete(folder_path)

    def test_notebook_create(self):
        notebook_path = 'users/gsbot/_created_by_test.ipynb'
        code          = "2+40"
        new_notebook  = self.api.notebook_create(notebook_path,code)
        assert new_notebook.get('path') == notebook_path
        assert self.api.file_delete(notebook_path) is True


    def test_notebook_content(self):
        self.result = self.api.notebook_content(self.notebook_name)

    def test_notebook_cells(self):
        self.result = self.api.notebook_cells(self.notebook_name)

    def test_notebook_codes_source(self):
        self.result = self.api.notebook_codes_source(self.notebook_name)


    def test_url(self):
        assert self.api.url('aaa') == 'http://localhost:8888/api/aaa'
        assert self.api.url('/aa') == 'http://localhost:8888/api/aa'
        assert self.api.url('a/a') == 'http://localhost:8888/api/a/a'
        assert self.api.url(     ) == 'http://localhost:8888/api/'
        assert self.api.url(None ) == 'http://localhost:8888/api/'

        assert self.api.url('/api'    ) == 'http://localhost:8888/api/api'
        assert self.api.url('/api/'   ) == 'http://localhost:8888/api/'
        assert self.api.url('/api/aaa') == 'http://localhost:8888/api/aaa'
        assert self.api.url('/apiaaa' ) == 'http://localhost:8888/api/apiaaa'