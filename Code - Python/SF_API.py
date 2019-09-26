import requests

class SalesforceAPIBangBang:
    params = {
    "grant_type": "password",
    "client_id": "3MVG9A2kN3Bn17hsrpOsFheLtoVuDSzn7rBDLdHndx1K9XZHPJAt0pfQaIy.v5azYK2g8PSWJifdtyQ47Ctlu", # Consumer Key
    "client_secret": "9204510300379643779", # Consumer Secret
    "username": "sanket_vaidya@hotmail.com", # The email you use to login
    "password": "BePositive1!azEIY9N1VacO1Ps7uandxiFj5" # Concat your password and your security token
    }
    access_token = ''
    instance_url = ''
    
    def __init__(self):
        print("• Initializing SF_API")
        r = requests.post("https://login.salesforce.com/services/oauth2/token", params=self.params)
        self.access_token = r.json().get("access_token")
        self.instance_url = r.json().get("instance_url")
        print("• Access Token:", self.access_token)
        print("• Instance URL", self.instance_url)
        print("• Response : " , r)

    def sf_api_call(self, action, parameters = {}, method = 'get', data = {}):
        """
        Helper function to make calls to Salesforce REST API.
        Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
        """
        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.access_token
        }
        if method == 'get':
            r = requests.request(method, self.instance_url+action, headers=headers, params=parameters, timeout=30)
        elif method in ['post', 'patch']:
            r = requests.request(method, self.instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
        else:
            # other methods not implemented in this example
            raise ValueError('Method should be get or post or patch.')
        print('Debug: API %s call: %s - StatusCode %s' % (method, r.url, r.status_code) )    
        
        if r.status_code < 300:
            if method=='patch':
                return None
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
