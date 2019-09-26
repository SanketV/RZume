import csv
import requests
params = {
    "grant_type": "password",
    "client_id": "3MVG9FS3IyroMOh6kcLgYOf5qUWRieofUkdkebMP7qwwqaNC8bP_9HIeWsyPfKYjS3vmKZpJQJLtuaFbvKHGp", # Consumer Key
    "client_secret": "BBFA7D464EF0BBBB713EA1007BBF03B207DE89495AE2058B4A6E2513ADB62ECA", # Consumer Secret
    "username": "sanket.vaidya@texascapitalbank.com.uat1", # The email you use to login
    "password": "Plano1234." # Concat your password and your security token
}
r = requests.post("https://test.salesforce.com/services/oauth2/token", params=params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)
print("response : " , r)

class Folder:
    id = ''
    label = ''
    name = ''
    type = ''
    url = ''
    folderSharesUrl = ''
    shares = []

class Shares:
    accessType = ''
    shareId = ''
    shareType = ''
    sharedWithId = ''
    sharedWithLabel = ''
    
    

def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
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
        

foldersJSON = sf_api_call('/services/data/v46.0/folders?page=1&pageSize=300')

folders = foldersJSON["folders"]

foldersList = []

counter = 1

for f in folders:
    
    counter = counter + 1
    
    fld = Folder()
    fld.id = f['id']
    fld.label = f['label']
    fld.name = f['name']
    fld.type = f['type']
    fld.url = f['url']
    
    folderSharesUrl = sf_api_call(f['url'])['sharesUrl']
    fld.folderSharesUrl = folderSharesUrl
    
    folderShares = sf_api_call(folderSharesUrl)["shares"]

    fldSharesList = []    
        
    for fs in folderShares:
        fldShare = Shares()
        fldShare.accessType = fs['accessType']
        fldShare.shareType = fs['shareType']
        fldShare.shareId = fs['shareId']
        fldShare.sharedWithId = fs['sharedWithId']
        fldShare.sharedWithLabel = fs['sharedWithLabel']
        fldSharesList.append(fldShare)
    
    fld.shares = fldSharesList
    foldersList.append(fld)

        #print("• Share : " + fldShare.accessType + ' , ' + fldShare.shareType + ' - ' + fldShare.sharedWithLabel)
    
   
def make_csv(foldersList):
    with open('data\SF Folder Lists and Shares.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['FolderName',
                         'FolderType',
                         'Url',
                         'FolderSharesUrl',
                         'SharedWith',
                         'ShareType',
                         'AccessType'])
        
        for fld in foldersList:
            for fldShare in fld.shares:
                writer.writerow([fld.label, 
                                 fld.type,
                                 fld.url,
                                 fld.folderSharesUrl,
                                 fldShare.sharedWithLabel,
                                 fldShare.shareType,
                                 fldShare.accessType])
                print('• ' + fld.label + ' - ' + fldShare.sharedWithLabel)
                
make_csv(foldersList)
 
