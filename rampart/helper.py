import os

def file_path(name, image=None, sound=None):
    if image is not None:
        fullname = os.path.join("assets","images",name)
    if sound is not None:
        fullname = os.path.join("assets","sounds",name)
    return fullname