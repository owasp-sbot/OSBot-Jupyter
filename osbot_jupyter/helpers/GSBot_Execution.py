from osbot_aws.apis.Lambda import Lambda


class GSBot_Execution:

    def __init__(self):
        self._lambda = Lambda('osbot.lambdas.osbot')

    def invoke(self,command):
        payload = {'team_id': 'T7F3AUXGV',
                   'event': {'type': 'message',
                             'text': command,
                             'channel': 'GDL2EC3EE',
                             'user': 'U7ESE1XS7'}}

        return self._lambda.invoke(payload)