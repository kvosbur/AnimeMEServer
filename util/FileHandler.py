import uuid
import base64
import os.path
import shutil

folderPath = "Now set in .env and read in during app.py setup"
urlBase = "https://kevinvosburgh.com/AnimeME/"


def base64WriteFile(image64, location):
    filePath = location + "/" + str(uuid.uuid4()) + ".jpeg"
    path = os.path.join(folderPath, filePath)
    try:
        imageFile = open(path, "w+b")
        # print(type(imageFile))
        imageFile.write(base64.b64decode(image64))
        imageFile.close()
        return urlBase + filePath
    except Exception as e:
        print(e)
        return {"message": "Could not save the image", "statusCode": -1}, 400


# Returns the complete file path for a given url
def getFilePath(url):
    if url is None or url == "":
        return ""
    return url.replace(urlBase, folderPath, 1)


# Returns the url for a given file a path
def getUrlFromPath(path):
    return path.replace(folderPath, urlBase, 1)


# Returns the complete file path given a uuid, location
def getCompleteFilePath(fileName, location):
    filePath = location + "/" + fileName + ".jpeg"
    path = os.path.join(folderPath, filePath)
    return path


# Delete the path at given path
def deleteFile(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


# Copies the path at source and writes at dest
def copyFile(source, dest):
    shutil.copyfile(source, dest)
    return
