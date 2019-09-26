import csv
import pprint as pp
from SF_API import SalesforceAPIBangBang

class Folder:
    id = ''
    label = ''
    name = ''
    type = ''
    url = ''
    folderSharesUrl = ''
      
salesforceAPI = SalesforceAPIBangBang()
foldersJSON = salesforceAPI.sf_api_call(action='/services/data/v46.0/folders?page=1&pageSize=300')

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
    
    foldersList.append(fld)

print("\n\n ♠ Folders List : \n")
   
def make_csv(foldersList):
    with open('data\\01 SF Folder Lists.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['FolderName',
                         'FolderId',     
                         'FolderType'
                         ])
        
        for fld in foldersList:
            writer.writerow([fld.label, 
                             fld.id,
                             fld.type
                             ])
            print('• ' + fld.label )
                
make_csv(foldersList)

