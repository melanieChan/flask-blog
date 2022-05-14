import os
import requests

local_path = os.path.abspath(os.path.dirname(__file__)) # finds project directory

# downloads a database file to the project directory
def download_database():
    file_url = "https://github.com/melanieChan/app-data/blob/flask-blog-sqlalchemy/database.db?raw=true"

    request = requests.get(file_url, stream = True) # get data
    download_destination = os.path.join(local_path, 'database.db') # set a path for the new file

    # load data in small sections
    with open(download_destination,"wb") as db_file:
        for chunk in request.iter_content(chunk_size=1024):
             if chunk:
                 db_file.write(chunk)

def get_db_path():
    dir_path = os.path.abspath(os.path.dirname(__file__)) # path of current file's directory

    # check if there's a file named database.db
    db_file_path = os.path.join(dir_path, 'database.db')
    db_file_exists = os.path.isfile(db_file_path)

    if not db_file_exists: # download the database if it doesn't already exist
        download_database()

    return db_file_path
