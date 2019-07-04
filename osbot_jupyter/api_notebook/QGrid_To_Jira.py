from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_jira.api.jira_server.API_Jira import API_Jira


class QGrid_To_Jira:
    def __init__(self, grid):
        self.grid = grid
        self.api_jira = API_Jira()
        self.api_jira_rest = API_Jira_Rest()

    def jira_update_issue_status(self, key, value):
        transitions = self.api_jira.issue_next_transitions(key)
        transitions_id = transitions.get(value)
        if transitions_id is None:
            return {'status': 'error', 'data': 'transition not available: {0}'.format(value)}
        result = self.api_jira.jira().transition_issue(key, transitions_id)

        return {'status': 'ok', 'data': result}

    def jira_remove_links_to_target(self, from_id, link_type, to_id):
        issue_links = self.api_jira.issue_links(from_id).get(link_type)
        if issue_links:
            for issue_link in issue_links:
                if to_id == issue_link.get('Key'):
                    link_id = issue_link.get('Id')
                    print('deleting link', from_id, link_type, link_id)
                    self.api_jira.issue_delete_link(link_id)
                    return True
        # return False
        return True  # to handle cases when a mistaske is made on the new issue link type

    def jira_update_issue_link(self, issue_id, to_id, old_link_issue, new_link_issue):
        if self.jira_remove_links_to_target(issue_id, old_link_issue, to_id) is False:
            print('removing link failed', issue_id, old_link_issue, to_id)
            return {'status': 'error', 'data': 'removing link failed'}
        try:
            self.api_jira.issue_add_link(issue_id, new_link_issue, to_id)
            print('added link', issue_id, new_link_issue, to_id)
            return {'status': 'ok', 'data': 'issue link edited'}
        except Exception as error:
            print('Failed to add link', issue_id, new_link_issue, to_id)
            print('{0}'.format(error))
            return {'status': 'error', 'data': 'adding link failed (after removing link)'}

    def jira_update_field(self, key, field, value):
        if not value:
            result = {'status': 'error', 'data': 'empty values not supported'}
        else:
            value = value.strip()
            if field == 'Latest_Information': field = 'Latest Information'
            if field == 'Status':
                result = self.jira_update_issue_status(key, value)
            else:
                data = self.api_jira_rest.issue_update_field(key, field, value)
                if data is False:
                    result = {'status': 'error', 'data': data}
                else:
                    result = {'status': 'ok', 'data': data}
            result['key'] = key
            result['field'] = field
            result['value'] = value

        return result

    def setup(self):
        def on_value_change(event, qgrid_widget):
            key = event.get('index')
            field = event.get('column')
            value = event.get('new')
            print("updating field `{0}` with value `{1}` on issue `{2}".format(field, value, key))
            result = self.jira_update_field(key, field, value)
            print(result)

        self.grid.on('cell_edited', on_value_change)
        return self