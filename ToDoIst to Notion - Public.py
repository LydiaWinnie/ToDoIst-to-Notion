import todoist

##You need the title of your Notion Dashboard to be "Task"
##You need a date column of your Notion Dashboard to be "Date"
##You need a multi-select column of your Notion Dashboard to be "Dashboard" and should have already created the "ToDoIst" option on Notion
##### ALL OF THE VALUES YOU PASTE HERE SHOULD BE IN STRINGS
TODOIST_API_KEY =24b4b3c643eb88c309d8d9be1e024b464f5cba9d
TODOIST_label_id =2168717601
NOTION_API_KEY = secret_AFDPWr0u4UGRZwbZ4PtUbbDMzf7NOKiQdBpzaUBMIHI
database_id =619ad07ab6024d05b65b1b9649147a26



api = todoist.TodoistAPI(TODOIST_API_KEY)
api.sync()

import requests
resultList=requests.get(
    "https://api.todoist.com/rest/v1/tasks",
    params={
        "label_id": TODOIST_label_id
    },
    headers={
        "Authorization": "Bearer %s" % TODOIST_API_KEY
    }).json()


taskData = []

import os
from notion_client import Client
from pprint import pprint
from datetime import datetime

os.environ['NOTION_TOKEN'] = NOTION_API_KEY
notion = Client(auth=os.environ["NOTION_TOKEN"])

for result in resultList:
    print(result)
    print("\n")

    taskName = result['content']
    dueDate = result['due']['date']

    #Enter the task into Notion
    my_page = notion.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            "properties": {
                'Task': {
                    "type": 'title',
                    "title": [
                    {
                        "type": 'text',
                        "text": {
                        "content": taskName,
                        },
                    },
                    ],
                },
                'Date': {
                    "type": 'date',
                    'date': {
                        'start': dueDate, 
                        'end': None,
                    }
                },
                'Dashboard':  {
                    "type": 'multi_select', 
                    'multi_select': [{
                        "name": "ToDoIst"
                    }],
                },
            },
        },
    )

    #Delete the task from ToDoIst (the api stuff is defined in the first 3 lines of the program)

    item = api.items.get_by_id(result['id'])
    item.delete()
    api.commit()

    
