from unittest import TestCase

from pbx_gs_python_utils.utils.Dev            import Dev
from osbot_jupyter.api_notebook.Jp_Graph_Data import Jp_Graph_Data


class test_Jp_Graph_Data(TestCase):

    def setUp(self):
        self.jp_graph_data = Jp_Graph_Data()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_issue(self):
        issue_id = 'RISK-12'
        assert self.jp_graph_data.issue(issue_id).get('Key') == issue_id

    def test_issues(self):
        issues_ids = ['RISK-12','RISK-234']
        self.result = list(set(self.jp_graph_data.issues(issues_ids))) == issues_ids


    def test_jira_links(self):
        depth         = 1
        key           = 'RISK-1610'
        direction     = 'all'
        graph  = self.jp_graph_data.jira_links(key, direction, depth)
        assert len(graph.nodes) > 5
        assert len(graph.edges) > 5

    def test_graph_expand(self):
        depth         = 1
        key           = 'RISK-1610'
        link_types    = 'has RISK'
        graph  = self.jp_graph_data.graph_expand(key, depth, link_types)
        assert len(graph.nodes) == 7
        assert len(graph.edges) == 6
