import couchdb
import argparse
from utils import *

# just for adding views designdoc map reduce fucntions to specified database
if __name__ == '__main__':
    # add argument
    paser = argparse.ArgumentParser()
    paser.add_argument("--dbname", type=str, default="tweets", help="The name of the database you wan to store")
    paser.add_argument("--views", type=str, default="./views", help="The path of the views file")
    arg = paser.parse_args()

    couch = couchDataBase('http://admin:admin@172.26.132.194:5984/', arg.dbname)
    design = f"design_{couch.db_name}"
    couch.createView(design, arg.views) # might have different views for different scenario

    pass

