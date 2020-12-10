from fastapi import (
    FastAPI,
    File,
    UploadFile
)
# import config # used for local debugging
# import uvicorn # used for local debugging
from . import config
import tempfile
import hashlib
import zipfile
import re
import os
from collections import Counter
from pathlib import Path

settings = config.Settings()
app = FastAPI()

urlRegex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'
emailRegex = r'(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))'



def tree(dir_path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    # this took too much time to find. thanks SO
    space =  '    '
    branch = '│   '
    tee =    '├── '
    last =   '└── '
    contents = list(dir_path.iterdir())
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            yield from tree(path, prefix=prefix+extension)

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

def build_dir_tree(z):
    with tempfile.TemporaryDirectory() as temp_dir:
        z.extractall(temp_dir)
        built_tree = tree(Path(temp_dir))
        tree_str = ''
        for f in built_tree:
            tree_str += f + '\n'

    return tree_str

def string_finder(filebytes):
    with tempfile.NamedTemporaryFile() as temp_zip:
        zip_file = temp_zip.name
        with open(zip_file, "wb") as f:
            f.write(filebytes)
        urls = []
        emails = []

        with zipfile.ZipFile(zip_file, "r") as z:
                paths = z.namelist()
                tree = build_dir_tree(z)
                count = len(z.infolist())
                ext_count = Counter((ext for base, ext in (os.path.splitext(fname) for fname in paths)))
                for path in paths:
                    if path.endswith('.php'):
                        with z.open(path, "r") as f:
                            text = f.read().lower().decode('utf-8', 'ignore')

                        um = tuple(m.group(0) for m in re.finditer(urlRegex, text) if m.group(0))
                        em = tuple(m.group(0) for m in re.finditer(emailRegex, text) if m.group(0))

                        for u in um:
                            urls.append(u)
                        for e in em:
                            emails.append(e)


    strings_out = {
        'ext_count': ext_count,
        'tree': tree,
        'total_files': count,
        'urls': set(urls),
        'emails': set(emails)
    }

    return strings_out

@app.post("/api/analyze")
async def analyze(file: bytes = File(...)):
    hashes = hash_file(file)
    strings = string_finder(file)

    out = {
        "file_size": len(file),
        "hashes": hashes,
        "strings": strings
    }
    return out