import os
from fastapi import HTTPException


def read_file(path: str):
    if not path.startswith("/data/"):
        return {"error": "Access restricted"}

    if not os.path.exists(path):
        return {"error": "File not found"}

    with open(path, "r") as f:
        content = f.read()

    return {"content": content}