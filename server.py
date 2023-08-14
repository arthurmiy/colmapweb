from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os
from tusserver.tus import create_api_router
from pydantic import BaseModel
from threading import Thread

class Project(BaseModel):
    name: str


def writeStatusJson():
    # Data to be written
    dictionary = {
        "name": "sathiyajith",
        "rollno": 56,
        "cgpa": 8.6,
        "phonenumber": "9976770500"
    }
 
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

def processData (folderName):
    print(folderName)
    writeStatusJson()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

@app.get("/pjts")
def read_item():
    folder = fast_scandir("projects")
    return folder

@app.post("/pjt")
def createPjtStructure (pjt: Project):
    #todo copy files to name/imgs folder
    background_thread = Thread(target=processData, args=(pjt.name,))
    background_thread.start()
    return "Success"





