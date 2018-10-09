from PIL import Image
import os, sys

class Loader(object):

    def __init__(self, d):
        self.directory = d 

    def __call__(self):
        print '__call__'


def main():
    if __name__=='__main__':
        sys.exit(main())
