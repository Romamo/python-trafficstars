from datetime import datetime, timedelta
import logging
import requests

# logger
logger = logging.getLogger(__name__)


class TrafficstarsException(Exception):
    pass


class Trafficstars(object):
    access_token = None
    refresh_token = None
    token_type = None
    expires = None
    version = '1'
    client_id = None
    client_secret = None
    username = None
    password = None

    def __init__(self, client_id, client_secret, username=None, password=None, version='1'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    def auth(self):
        if not self.expires:
            result = self.request('auth/token', 'post', params=dict(grant_type='password',
                                                                    client_id=self.client_id,
                                                                    client_secret=self.client_secret,
                                                                    username=self.username,
                                                                    password=self.password))

            self.expires = datetime.now() + timedelta(seconds=result['expires_in'])
            self.access_token = result['access_token']
            self.refresh_token = result['refresh_token']
            self.token_type = result['token_type']
            # else self.expires > datetime.now():
            #     pass

    def request(self, command, method='get', placeholders=None, params=None):
        url = u"https://api.trafficstars.com/v{version}/{command}".format(version=self.version, command=command)
        if placeholders:
            url += u'/{}'.format(u'/'.join(map(str, filter(None, list(placeholders)))))

        if self.token_type:
            headers = dict(Authorization="{} {}".format(self.token_type, self.access_token))
        else:
            headers = None

        response = requests.request(method, url, params=params, headers=headers)
        if response.status_code == 200:
            # result = json.loads(response.content)
            return response.json()
        raise TrafficstarsException(response.content)

    def process(self, command, method, *args, **kwargs):
        self.auth()
        result = self.request(command, method, args, kwargs)
        return result

    def __getattr__(self, name, *args, **kwargs):
        if name.find('_') > 0:
            return self.__call__(name.replace('_', '/'), *args, **kwargs)
        raise TrafficstarsException(u"Method {} not allowed".format(name))

    def campaign_status(self, id):
        return self.process('campaign/status', 'get', id)

    def campaign_list(self, **kwargs):
        return self.process('campaign/list', 'get', **kwargs)

    def stats_advertiser(self, section, section_id=None, **kwargs):
        return self.process('stats/advertiser', 'get', section, section_id, **kwargs)

    def banner_list(self, **kwargs):
        return self.process('banner/list', 'get', **kwargs)
