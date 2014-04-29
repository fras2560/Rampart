'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 29/04/2014
@note: random helper functions
'''
import os


def file_path(name, image=None, sound=None):
    '''
    a function to helper find the filepath of the asset
    Parameters:
        name: the name of file
        image: a boolean to specify if an image file or not
        sound: a boolean to specify if an sound file or not
    '''
    if image is not None:
        fullname = os.path.join("assets","images",name)
    if sound is not None:
        fullname = os.path.join("assets","sounds",name)
    return fullname