import json
import requests


class Jupyter_API:
    def __init__(self,server=None, token=None):
        self.server =  server
        self.token  = token

    # this is quite slow (simple requests taking 700ms to 1250ms
    def http_get(self, path):
        url = self.url(path)
        headers = {'Authorization': 'Token {0}'.format(self.token)}
        response = requests.get(url,headers=headers)
        if response.status_code != 404:
            return response.json()

    # trying to debug why http_get is so slow (each request takes at least 1 sec
    # def http_get(self, path):
    #     from time import time
    #     start = time()
    #     url = self.url(path)
    #     headers = {'Authorization': 'Token {0}'.format(self.token)}
    #     from pbx_gs_python_utils.utils import Http
    #     data = Http.GET(url,headers)
    #     duration = time() - start
    #     print('took {0:.2f} in http_get'.format(duration))
    #     return json.loads(data)
    #
    #     response = requests.get(url,headers=headers)
    #     if response.status_code != 404:
    #
    #         duration = time() - start
    #         print('took {0:.2f} in http_get'.format(duration))
    #         return response.json()

    def http_delete(self, path):
        url = self.url(path)
        headers = {
                'Authorization': 'Token {0}'.format(self.token)}
        response = requests.delete(url,headers=headers)
        if response.status_code != 404:
            if response.text != '':
                return response.json()
            return {}

    def http_patch(self, path, data):
        url = self.url(path)
        headers = {
                'Authorization': 'Token {0}'.format(self.token),
                'Content-Type' :  'application/json' }
        response = requests.patch(url,data=json.dumps(data), headers=headers)
        if response.status_code != 404:
            return response.json()

    def http_post(self, path, data):
        url = self.url(path)
        headers = {
                'Authorization': 'Token {0}'.format(self.token),
                'Content-Type' :  'application/json'
                    }
        response = requests.post(url,data=json.dumps(data), headers=headers)
        if response.status_code != 404:
            return response.json()

    def http_put(self, path, data):
        url = self.url(path)
        headers = {
                'Authorization': 'Token {0}'.format(self.token),
                'Content-Type' :  'application/json'
                    }
        response = requests.put(url,data=json.dumps(data), headers=headers)
        if response.status_code != 404:
            return response.json()


    # methods

    def contents(self,target=None):
        path = 'api/contents'
        if target:
            path = '{0}/{1}'.format(path,target)
        return self.http_get(path)

    def directory_contents(self, path_root=''):
        from time import time
        start = time()
        files   = []
        folders = []
        data = self.contents(path_root)
        if data is not None:
            if type(data) is str:
                print(data)
            if data.get('type') == 'directory':
                for item in data.get('content'):
                    name = item.get('name')
                    path = item.get('path')
                    url  = "{0}/tree/{1}".format(self.server, item.get('path'))
                    if item.get('type') == 'directory':
                        folders.append({'name':  name, 'path': path, 'url': url, })
                    else:
                        files.append({'name': name, 'path': path, 'url': url, })
        duration = time() - start
        print('took {0:.2f} secs to get path: {1}'.format(duration,path_root))

        return {'files': files, 'folders': folders}

    # this won't work like this (too slow to get each folder contents
    # def directory_contents_recursive(self, path_root=''):
    #     all_files   = []
    #     from time import time
    #     start = time()
    #     print('----')
    #     def process_folder(path):
    #         data = self.directory_contents(path)
    #         #for file in data.get('files'):
    #         #    all_files.append(file.get('path'))
    #         for folder in data.get('folders'):
    #             process_folder(folder.get('path'))
    #             break
    #     print('----')
    #     process_folder(path_root)
    #     duration = time() - start
    #     print('took {0:.2f} in directory_contents_recursive'.format(duration))
    #     return all_files

    def file_delete(self, path):
        contents_path = 'contents/{0}'.format(path)
        if self.http_delete(contents_path) == {}:
            return True
        return False

    # def folder_create(self,path):
    #     folder_path = 'contents/{0}'.format(path)
    #     config = {'type': 'directory'}
    #     return self.http_post(folder_path,config)

    def folder_create(self, path, contents=None):
        notebook_path = 'contents/{0}'.format(path)
        config = { 'type': 'directory' }
        return self.http_put(notebook_path, config)

    # def file_create(self,path):
    #     file_path = 'contents/{0}'.format(path)
    #     config = {'type': 'file'}
    #     return self.http_post(file_path,config)

    def file_create(self, path, contents=None):
        file_path = 'contents/{0}'.format(path)
        config = {
                    'type'    : 'file',
                    'format'  : 'text',
                    'content' : contents
                }
        try:                                                                # todo: refactor with similar code below
            result = self.http_put(file_path, config)
            if result.get('message'):
                return {'status': 'error', 'data': result.get('message')}
            else:
                return {'status': 'ok', 'path': result.get('path')}
        except Exception as error:
            return {'status': 'error', 'data': '{0}'.format(error)}

    # def notebook_create(self,path):
    #     notebook_path = 'contents/{0}'.format(path)
    #     config = {'type': 'notebook'}
    #     return self.http_post(notebook_path,config)

    def kernels(self):
        items = {}
        for kernel in self.http_get('api/kernels'):
            items[kernel.get('id')] = kernel
        return items


    def notebook_create(self, path, code=None):
        if code:
            cells = [{  "cell_type"         : "code",
                        "source"            : [code],
                         "execution_count"  : None,
                         "metadata"         : {},
                         "outputs"          : []}]
        else:
            cells = []


        notebook_path = 'contents/{0}'.format(path)
        config = {
                    'type'    : 'notebook',
                    'format'  : 'text',
                    'content' : {
                                     "cells"         : cells,
                                     "metadata"      : {},
                                     "nbformat"      : 4,
                                     "nbformat_minor": 2
                                }
                }
        try:
            result = self.http_put(notebook_path, config)
            if result.get('message'):
                return {'status' : 'error', 'data': result.get('message') }
            else:
                return {'status': 'ok', 'path': result.get('path')}
        except Exception as error:
            return {'status': 'error', 'data': '{0}'.format(error)}


    def notebook_content(self,path):
        return self.contents(path).get('content')

    def notebook_cells(self,path):
        return self.notebook_content(path).get('cells')

    def notebook_codes_source(self,path):
        codes_source = []
        for cell in self.notebook_content(path).get('cells'):
            if cell.get('cell_type') == 'code':
                codes_source.append(cell.get('source'))
        return codes_source

    def notebook_exists(self,path):
        return self.contents(path) is not None

    def status(self):
        return self.http_get('status')

    def url(self,path=None):
        if   path is None or len(path) == 0: path = '/'
        elif path[0] != '/'                : path = '/' + path

        if path.startswith('/api/') is False: path = '/api{0}'.format(path)

        return "{0}{1}".format(self.server,path)

    def version(self):
        return self.http_get('')




    # experimental
    def kernel_code_execute(self,code_to_execute):

        from websocket import create_connection
        import uuid
        import datetime

        kernel_id = list(set(self.kernels())).pop()
        headers   = {'Authorization': 'Token {0}'.format(self.token)}
        url       = "ws://localhost:8888/api/kernels/{0}/channels".format(kernel_id)
        ws        = create_connection(url, header=headers)

        def send_execute_request(code):
            msg_type = 'execute_request';
            content = {'code': code, 'silent': False}


            hdr = {'msg_id': uuid.uuid4().hex,
                   'username': 'test',
                   'session': uuid.uuid4().hex,
                   'data': datetime.datetime.now().isoformat(),
                   'msg_type': msg_type,
                   'version': '5.0'}
            msg = {'header': hdr, 'parent_header': hdr,
                   'metadata': {},
                   'content': content}
            return msg

        ws.send(json.dumps(send_execute_request(code_to_execute)))
        messages = []
        msg_type = ''
        while msg_type != "execute_reply":
            rsp         = json.loads(ws.recv())
            content     = rsp.get("content")
            msg_type    = rsp.get("msg_type")
            messages.append({'msg_type': msg_type, 'content': content})
        ws.close()

        return messages