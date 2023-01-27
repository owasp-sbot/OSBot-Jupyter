from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_jupyter.api_notebook.Jp_Helper import Jp_Helper
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
        return subprocess.run(puml_params)

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

    def show_png_for_graph_schema(self, hb_jira_slack):
        jira_graph      = hb_jira_slack.jira_graph_jql.jira_graph
        jira_graph_view = Jira_Graph_View(jira_graph=jira_graph)
        schema_graph    = jira_graph_view.create_schema_graph()
        schema_graph.set_skin_param('linetype', 'polyline')
        schema_graph.render_puml(using_jira_nodes=False)
        puml_code = schema_graph.get_puml()
        self.show_png_from_puml_code(puml_code)

    def show_png_for_graph(self, hb_jira_slack):
        jira_graph_jql = hb_jira_slack.jira_graph_jql
        jira_graph_jql.render_puml_from_jira_graph()
        puml_code = jira_graph_jql.jira_graph.get_puml()
        self.show_png_from_puml_code(puml_code)

    def show_png_from_puml_code(self, puml_code):
        result    = self.puml_to_png(puml_code)
        png_file  = result.get('png_file')
        Jp_Helper().show_png_file_binary(png_file)