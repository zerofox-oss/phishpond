from fastapi import (
    FastAPI,
    File,
    UploadFile
)
# import config # used for local debugging
# import uvicorn # used for local debugging
from . import config
import hashlib
import zipfile
import re
import os

settings = config.Settings()
app = FastAPI()

urlRegex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'
emailRegex = r'(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))'


def hash_file(filebytes):
    sha1 = hashlib.sha1(filebytes).hexdigest()
    sha256 = hashlib.sha256(filebytes).hexdigest()
    md5 = hashlib.md5(filebytes).hexdigest()

    hash_out = {
        "sha1": sha1,
        "sha256": sha256,
        "md5": md5
    }

    return hash_out


def string_finder(filebytes):
    with open("test.zip", "wb") as f:
        f.write(filebytes)

    zip_file = "test.zip"

    urls = []
    emails = []

    with zipfile.ZipFile(zip_file, "r") as z:
            paths = z.namelist()

            for path in paths:
                if path.endswith('.php'):
                    with z.open(path, "r") as f:
                        text = f.read().lower().decode('utf-8')

                    um = tuple(m.group(0) for m in re.finditer(urlRegex, text) if m.group(0))
                    em = tuple(m.group(0) for m in re.finditer(emailRegex, text) if m.group(0))

                    for u in um:
                        urls.append(u)
                    for e in em:
                        emails.append(e)
 
    os.remove("test.zip")

    strings_out = {
        "urls": set(urls),
        "emails": set(emails)
    }
    
    return strings_out

@app.post("/analyze")
async def analyze(file: bytes = File(...)):
    hashes = hash_file(file)
    strings = string_finder(file)

    out = {
        "file_size": len(file),
        "hashes": hashes,
        "strings": strings
    }
    return out


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=5000) # local debugging
