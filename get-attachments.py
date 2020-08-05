import requests
import re
import csv
import os
parent_dir = "AzDo_Backup"
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)
with open('work-items-with-attachments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:        
        url_name = "https://dev.azure.com/[Organization Name]/[Team Project Name]/_apis/wit/workitems/" + row['ID'] + "?api-version=5.1&$expand=Relations"
        sanitized_title = re.sub('[^a-zA-Z0-9 \n\.\-]', '', row['Title']).strip()
        folder_name = row['ID']+' - '+ sanitized_title
        print(folder_name) 
        path = os.path.join(parent_dir, folder_name) 
        os.mkdir(path) 
        #print(url_name)
        r = requests.get(url_name, auth=('[user name]', '[pat token]'))
        out = r.json()
        for item in out['relations']:
            if(item['rel'] == 'AttachedFile'):
                download_url = item['url']
                print(download_url)
                #filename = item['attributes']['name']
                filename = os.path.join(path, item['attributes']['name'])
                print(filename)
                attachment = requests.get(download_url,auth=('[user name]', '[pat token]'))
                with open(filename, 'wb') as f:
                    f.write(attachment.content)
