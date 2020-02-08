from time import sleep
import qgrid
import pandas as pd
import ipywidgets as widgets
from osbot_jupyter.api_notebook.QGrid_To_Jira import QGrid_To_Jira
from osbot_jira.api.API_Issues import API_Issues

class Edit_UI():

    def __init__(self, issue_id=None, issues=None):
        self.issue_id      = issue_id
        self.issues        = issues
        self.columns       = ['Key', 'Summary', 'Issue Link', 'Description', 'Status'] # 'Latest_Information'
        self.projects      = ['TASK', 'OUTCOME', 'KEYRESULT', 'QUESTION']
        self.issue_types   = ['Task', 'Outcome', 'KeyResult', 'Question']
        self.link_types    = ['is delivered by', 'is parent of', 'uses']
        self.qgrid_to_jira = QGrid_To_Jira(None)
        self.api_jira      = self.qgrid_to_jira.api_jira
        self.api_jira_rest = self.qgrid_to_jira.api_jira_rest
        self.api_issues    = API_Issues()

    def ui_add_issue(self):
        self.dropdown_project = widgets.Dropdown(options=self.projects, description='Project')
        self.dropdown_issue_type = widgets.Dropdown(options=self.issue_types, description='Issue Type')
        self.dropdown_link_type = widgets.Dropdown(options=self.link_types, description='Link  Type')
        self.text_summary = widgets.Text(value='new_issue', description='Summary')
        self.button_create_issue = widgets.Button(description='Create Issue', icon='plus-square')

        def on_click_create_issue(b):
            self.on_create_issue()

        self.button_create_issue.on_click(on_click_create_issue)
        return widgets.HBox([self.dropdown_project, self.dropdown_issue_type,
                             self.dropdown_link_type, self.text_summary,
                             self.button_create_issue])

    def ui_link_issue(self):
        self.add_link_dropdown_issue_type = widgets.Dropdown(options=self.link_types, description='Link Type')
        self.add_link_text_issue_id = widgets.Text(value='', description='Issue Id')
        self.add_link_button_create_issue = widgets.Button(description='Link Issue', icon='link')

        def on_click_link_issue(b):
            self.on_link_issue()

        self.add_link_button_create_issue.on_click(on_click_link_issue)

        return widgets.HBox([self.add_link_dropdown_issue_type,
                             self.add_link_text_issue_id,
                             self.add_link_button_create_issue])

    def ui_load_issue(self):
        self.output_area = widgets.Output(layout={'border': '1px solid black', 'width': '1200px'})
        self.button_status = widgets.Button(description='...', layout=widgets.Layout(width='50%'))
        self.text_issue_id = widgets.Text(value=self.issue_id, description='Issue Id:')
        self.button_load = widgets.Button(description='Load Data', icon='download')
        self.button_load.style.button_color = 'lightblue'

        def on_button_clicked(b):
            self.issues = None              # to force data reload
            self.issue_id = self.text_issue_id.value
            self.button_status.style.button_color = 'orange'
            self.button_status.description = 'Loading Data from {0}'.format(self.issue_id)
            if self.create_grid():
                self.button_status.description = 'Done'
                self.button_status.style.button_color = 'lightgreen'

        self.button_load.on_click(on_button_clicked)

        return widgets.HBox([self.text_issue_id, self.button_load, self.button_status])

    def ui_add_grid(self):
        def on_value_change_local(event, qgrid_widget):
            self.on_value_change(event, qgrid_widget)

        self.grid = qgrid.show_grid(pd.DataFrame([]), grid_options={'maxVisibleRows': 100})
        self.grid.on('cell_edited', on_value_change_local)

        self.create_grid()
        return self.grid

    def show_ui(self, show_load_issue=True, show_add_issue=True, show_add_link=True, show_qgrid=True, show_output=True):
        items = []

        if show_load_issue: items.append(self.ui_load_issue())
        if show_add_link: items.append(self.ui_link_issue())
        if show_add_issue: items.append(self.ui_add_issue())
        if show_qgrid: items.append(self.ui_add_grid())
        if show_output: items.append(self.output_area)

        self.vbox = widgets.VBox(items)

        return self.vbox

    def on_create_issue(self):
        qgrid_to_jira = QGrid_To_Jira(None);
        with self.output_area:
            project = self.dropdown_project.value
            issue_type = self.dropdown_issue_type.value
            link_type = self.dropdown_link_type.value
            summary = self.text_summary.value
            status = '...'
            issue_id = self.issue_id
            print("Creating '{0}' issue in project '{1}' with summary '{2}', and link '{3}' to '{4}'".format(issue_type,
                                                                                                             project,
                                                                                                             summary,
                                                                                                             link_type,
                                                                                                             issue_id))
        try:
            # Create issue
            self.button_status.style.button_color = '#E59866'
            self.button_status.description = "Creating '{0}' issue in project '{1}'".format(issue_type, project)

            new_issue_id = qgrid_to_jira.api_jira.issue_create(project, summary, '', issue_type).key

            # Link issue
            self.button_status.style.button_color = 'orange'
            self.button_status.description = "Linking new issue '{0}' issue to '{1}'".format(new_issue_id, issue_id)

            qgrid_to_jira.api_jira.issue_add_link(issue_id, link_type, new_issue_id)

            # Update Grid
            self.button_status.style.button_color = 'darkorange'
            self.button_status.description = 'Adding new issue to grid'

            columns = list(self.grid.df.columns)
            new_row = [('Key', new_issue_id)]
            for name in columns:
                value = ''
                if name == 'Summary'   : value = summary
                if name == 'Issue Link': value = link_type
                new_row.append((name, value))
            self.grid.add_row(new_row)
                # [('Key', new_issue_id), ('Summary', summary), ('Latest_Information', ''), ('Description', ''),
                #  ('Status', status)])

            self.button_status.description = 'all done'
            self.button_status.style.button_color = 'lightgreen'
        except Exception as error:
            self.button_status.description = 'Error creating issue or link (see output area'
            self.button_status.style.button_color = 'pink'
            with self.output_area:
                print("{0}".format(error))

    def on_link_issue(self):
        from_key = self.issue_id
        link_type = self.add_link_dropdown_issue_type.value
        to_key = self.add_link_text_issue_id.value

        with self.output_area:
            try:
                result = self.api_jira.issue_add_link(from_key, link_type, to_key)
                self.button_status.style.button_color = 'lightgreen'
                self.button_status.description = 'Link added ok'
                self.issues = None
                self.create_grid()
                print(result)
            except Exception as error:
                print("Error: {0}".format(error))
                self.button_status.style.button_color = 'pink'
                self.button_status.description = 'Link Error (double check that the issue id exists)'

    def on_value_change(self, event, qgrid_widget):
        key = event.get('index')
        field = event.get('column')
        value = event.get('new')
        old = event.get('old')
        with self.output_area:
            # print(event)
            print("updating field '{0}' with value '{1}' on issue '{2}'".format(field, value, key))
        self.button_status.style.button_color = 'orange'

        qgrid_to_jira = QGrid_To_Jira(None);
        if field == 'Issue Link':
            with self.output_area:
                self.button_status.description = "Replacing Issue field {0} with {1}".format(old, value)
                result = qgrid_to_jira.jira_update_issue_link(self.issue_id, key, old, value)
        else:
            self.button_status.description = "Updating field {0} on {1}".format(field, key)
            result = qgrid_to_jira.jira_update_field(key, field, value)
        if result.get('status') == 'ok':
            self.button_status.style.button_color = 'lightgreen'
            self.button_status.description = 'Issue updated ok'
        else:
            self.button_status.style.button_color = 'pink'
            self.button_status.description = 'Update Error: {0}'.format(result.get('data'))

    def create_grid(self):
        if self.issue_id:
            try:
                # self.graph    = jira.graph_links(self.issue_id, 'all', 1)
                # self.df_graph = graph_table(self.graph,self.columns).fillna('')
                df_issues = self.get_issue_df()
                if len(df_issues) >0 :
                    self.grid.df = self.get_issue_df()
                    return True
                message = f"No links found for '{self.issue_id}'"
            except Exception as error:
                with self.output_area:
                    print('error :{0}'.format(error))
                message = 'Create Grid Error: {0}'.format(error)
            self.button_status.style.button_color = 'pink'
            self.button_status.description = message
        return False

    def get_issue_df(self):
        if self.issues is None:
            self.issues = self.get_issues()
        return pd.DataFrame(self.issues, columns=self.columns).set_index('Key').fillna('')


    def get_issues(self):
        root_issue = self.api_issues.issue(self.issue_id)
        if root_issue == {}:
            return []
        issues = [root_issue]
        issue_links = root_issue.get('Issue Links')
        for link_type, linked_issues in issue_links.items():
            for linked_issue in linked_issues:
                issue = self.api_issues.issue(linked_issue)
                issue['Issue Link'] = link_type
                issues.append(issue)
        return issues
