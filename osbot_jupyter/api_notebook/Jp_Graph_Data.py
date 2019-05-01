import json

from osbot_jira.api.API_Issues import API_Issues
from osbot_aws.apis.Lambda import Lambda
from osbot_jira.api.GS_Bot_Jira import GS_Bot_Jira
from osbot_jira.api.graph.Lambda_Graph_Commands import Lambda_Graph_Commands
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Graph_Data:

    def __init__(self):
        self.lambda_graph = Lambda('lambdas.gsbot.gsbot_graph')
        self.api_issues   = API_Issues()

    def lambda_invoke(self, params):
        result = self.lambda_graph.invoke( {'params': params , 'data': {}})
        return Misc.json_load(result)

    def issue(self,issue_id):
        return self.api_issues.issue(issue_id)

    def issues(self,issue_id):
        return self.api_issues.issues(issue_id)

    def jira_links(self,source, direction, depth):
        params = ['links',source, direction, depth]
        return GS_Bot_Jira().cmd_links(params, save_graph=False)

    def graph_expand(self, source, depth, link_types):
        params = [source, depth, link_types]
        return Lambda_Graph_Commands().expand(params=params,save_graph=False)

        #data = json..invoke(params))
        #nodes = data.get('nodes')
        #edges = data.get('edges')

