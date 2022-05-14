import os
import requests

local_path = os.path.abspath(os.path.dirname(__file__)) # finds project directory

# downloads a database file to the project directory
def download_database():
    file_url = "https://github.com/melanieChan/app-data/blob/flask-blog/database.db?raw=true"

    request = requests.get(file_url, stream = True) # get data
    download_destination = os.path.join(local_path, 'database.db') # set a path for the new file

    # load data in small sections
    with open(download_destination,"wb") as db_file:
        for chunk in request.iter_content(chunk_size=1024):
             if chunk:
                 db_file.write(chunk)
