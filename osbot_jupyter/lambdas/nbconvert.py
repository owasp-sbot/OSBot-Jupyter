from osbot_aws.Dependencies import load_dependency

#Not working: throwing issue: Cannot import name 'constants'",
def run(event, context):
    load_dependency('jupyter')
    #result = Process.run('jupyter')

    from runipy.notebook_runner import NotebookRunner
    from IPython.nbformat.current import read

    notebook = read(open("MyNotebook.ipynb"), 'json')
    return notebook
