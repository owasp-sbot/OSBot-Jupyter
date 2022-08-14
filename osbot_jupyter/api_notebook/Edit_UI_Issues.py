from osbot_jira.api.jira_server.API_Jira import API_Jira
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest


class Edit_UI_Issues:

    def __init__(self):
        #self.api_jira      = API_Jira()
        self.api_jira_rest = API_Jira_Rest()


    def issue(self, issue_id):
        return self.api_jira_rest.issue(issue_id) or {}

    def issue_links(self, issue):
        return issue.get('Issue Links') or {}

    def issue_links_ids(self, issue):
        links_ids = []
        for link_type, issues_ids in self.issue_links(issue).items():
            links_ids.extend(issues_ids)

        return links_ids

    # this method returns an array with the list of issue + linked issues (that are easy to load in Edit_UI qgrid
    #    if also has a special feature to add to the linked issues the issue link type from issue_id (as 'Issue Link')
    def issues(self, issue_id):
        root_issue = self.issue(issue_id)                                       # get root issue              (via rest api)
        if root_issue == {}:                                                    # if it doesn't exist
            return []                                                           # return an empty array
        linked_ids    = self.issue_links_ids(root_issue)                        # get all linked issues ids
        linked_issues = self.api_jira_rest.issues(linked_ids)                   # get all linked issues ids data (via rest api)

        issues = [root_issue]                                                   # array that will hold the result

        issue_links = root_issue.get('Issue Links').items()
        for link_type, linked_issue_ids in issue_links:                         # for each mapping in the 'Issue Links' field
            for linked_issue_id in linked_issue_ids:                            # for each issue_id linked
                issue = linked_issues.get(linked_issue_id) or {}                # get its data
                issue['Issue Link'] = link_type                                 # add the 'Issue Link' field
                issues.append(issue)                                            # add to the result array

        return issues


        # original code that used elastic
        # root_issue = self.api_issues.issue(self.issue_id)
        # if root_issue == {}:
        #     return []
        # issues = [root_issue]
        # issue_links = root_issue.get('Issue Links')
        # for link_type, linked_issues in issue_links.items():
        #     for linked_issue in linked_issues:
        #         issue = self.api_issues.issue(linked_issue)
        #         # issue = self.api_jira_rest.issue(linked_issue)  # much slower than using elk
        #         issue['Issue Link'] = link_type
        #         issues.append(issue)
        # return issues

    def summary(self, issue_id):
        return self.issue(issue_id).get('Summary')