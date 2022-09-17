from osbot_utils.utils.Files import temp_file, parent_folder, file_exists, file_to_base64
import subprocess

PATH_PLANTUML_JAR = '/usr/local/bin/plantuml.jar'

class Jp_Puml:

    def __init__(self, plantuml_jar=PATH_PLANTUML_JAR):
        self.plantuml_jar = plantuml_jar

    def exec_plantuml_jar(self, params=None):
        if type(params) is str:
            params = [params]
        process_name = 'java'
        puml_params = [process_name, '-jar', self.plantuml_jar, '-Xmx2512m',
                       '-DPLANTUML_LIMIT_SIZE=8192'                       ] + (params or [])
        subprocess.run(puml_params)

        # this was hanging the jupyter notebook cell, so using subprocess instead
        # exec_result  = exec_process(process_name, puml_params)
        # return exec_result.get('stdout') + exec_result.get('stderr')   # only one will have content

    # helper functions
    def version(self):
        return self.exec_plantuml_jar('-version')

    def puml_to_png(self, puml_code):
        puml_file = temp_file(extension=".puml", contents=puml_code)
        png_file = puml_file.replace(".puml", ".png")
        target_folder = parent_folder(puml_file)
        params = ['-tpng', '-o', target_folder, puml_file]
        exec_result = self.exec_plantuml_jar(params)
        if file_exists(png_file):
            return {'status': 'ok', 'png_file': png_file}
        else:
            return {'status': 'error', 'error': exec_result}

    def puml_to_base_64(self, puml_code):
        result = self.puml_to_png(puml_code)
        if result.get('status') == 'ok':
            return file_to_base64(result.get('png_file'))
        return None