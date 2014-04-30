'''
@author: Dallas Fraser
@contact: fras2560@mylaurier.ca
@version: 1.0
@date: 29/04/2014
@note: random helper functions
'''
import os
import unittest

def file_path(name, image=None, sound=None):
    '''
    a function to helper find the filepath of the asset
    Parameters:
        name: the name of file
        image: a boolean to specify if an image file or not
        sound: a boolean to specify if an sound file or not
    '''
    fullname = os.path.join("assets", name)
    if image is not None:
        fullname = os.path.join("assets","images",name)
    if sound is not None:
        fullname = os.path.join("assets","sounds",name)
    return fullname

class tester(unittest.TestCase):
    def setUp(self):
        self.fp = "tester"

    def tearDown(self):
        pass

    def test_file_path(self):
        result = file_path(self.fp)
        expected = os.path.join("assets",self.fp)
        self.assertEqual(result, expected)
        result = file_path(self.fp,image=True)
        expected = os.path.join("assets",'images',self.fp)
        self.assertEqual(result, expected)
        result = file_path(self.fp,sound=True)
        expected = os.path.join("assets",'sounds',self.fp)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()