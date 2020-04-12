from pbx_gs_python_utils.utils.Misc import Misc

from gw_bot.api.Slack_Commands_Helper import Slack_Commands_Helper
from osbot_aws.Dependencies import load_dependencies


# def load_dependency(target):
#     from pbx_gs_python_utils.utils.Files import Files
#     from osbot_aws.apis.S3 import S3
#     import shutil
#     import sys
#     s3         = S3()
#     s3_bucket  = 'gw-bot-lambdas'
#     s3_key     = 'lambdas-dependencies/{0}.zip'.format(target)
#
#     tmp_dir    = Files.path_combine('/tmp/lambdas-dependencies', target)
#     #return s3.file_exists(s3_bucket,s3_key)
#
#     if s3.file_exists(s3_bucket,s3_key) is False:
#         raise Exception("In Lambda load_dependency, could not find dependency for: {0}".format(target))
#
#     if Files.not_exists(tmp_dir):                               # if the tmp folder doesn't exist it means that we are loading this for the first time (on a new Lambda execution environment)
#         zip_file = s3.file_download(s3_bucket, s3_key,False)    # download zip file with dependencies
#         shutil.unpack_archive(zip_file, extract_dir = tmp_dir)  # unpack them
#         sys.path.append(tmp_dir)                                # add tmp_dir to the path that python uses to check for dependencies
#     return Files.exists(tmp_dir)


def run(event, context):
    try:
        load_dependencies('requests,syncer,pyppeteer,websocket-client')
        from osbot_jupyter.osbot.Jupyter_Commands import Jupyter_Commands
        params  = Misc.get_value(event, 'params',[])
        if not params: params = ['']
        data    = event.get('data')
        channel = Misc.get_value(data,'channel')
        team_id = Misc.get_value(data, 'team_id')
        params.append({"data": data } )
        return Slack_Commands_Helper(Jupyter_Commands).invoke(team_id, channel, params)
    except Exception as error:
        message = "[lambda_osbot] Error: {0}".format(error)
        #log_to_elk(message, level='error')
        return message