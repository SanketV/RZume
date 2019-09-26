import csv
import pandas as pd
import pprint
import json
from SF_API import SalesforceAPIBangBang

pp = pprint.PrettyPrinter(indent=4)


data = pd.read_csv(".\\data\\01 SF Folder Lists.csv")
folderNamesDict = dict(zip(data['FolderName'],data['FolderId']))

print(" • • • Folder Names List • • • ")
pp.pprint(folderNamesDict)

data = pd.read_csv(".\\data\\02 SF User Roles.csv")
userRolesDict = dict(zip(data['NAME'], data['ID']))

print("\n\n • • • User Roles List  • • • \n")
pp.pprint(userRolesDict)

salesforceAPI = SalesforceAPIBangBang()

def invokeSFFolderSharesAPI(folderId, shareList):
    #retrieve folder id
    #retreive user role id
    #create a post request
    foldersJSON = salesforceAPI.sf_api_call('/services/data/v46.0/folders/'+folderId+'/shares',
                                     method='post',
                                     data={"shares": shareList})
    pp.pprint(foldersJSON)    


inputData = pd.read_csv(".\\data\\Input-FolderName and New Roles.csv")
#pp.pprint(inputData)

for key, group_df in inputData.groupby('FolderName'):
    print("the group for folderName '{}' has {} rows".format(key,len(group_df)))
    shareList  = []
    for gRow in group_df.iterrows():
        
        roleId = userRolesDict[gRow[1]['ShareWith']]
        pp.pprint("• Role ID : " + roleId)
        
        if roleId is not None:        
            shareList.append({"shareWithId" : roleId, 
                          "shareType" : gRow[1]['ShareType'], 
                          "accessType" : gRow[1]['AccessType']})
    
    #pp.pprint(shareList)
    pp.pprint(json.dumps(shareList))

    folderId = folderNamesDict[key]     
    pp.pprint("Folder ID : " + folderId)
    
    
    invokeSFFolderSharesAPI(folderId, shareList)
    #pp.pprint(shareList)    
    

