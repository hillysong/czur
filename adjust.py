from PIL import Image
import os, sys

class Loader(object):

    def __init__(self, p):
        self.path = p 

    def __call__(self):
        files = [f for f in os.listdir(self.path) if f.startswith('image')]
        return sorted(files)


class ImageHandler(object):

    def __init__(self, images):
        self.list = images
        self.wmin = 10000
        self.hmin = 10000

    def __call__(self):
        self.smallest()
        #self.crop()

    def smallest(self):
        wminfile = ''
        hminfile = ''
        for i in self.list:
            im = Image.open(i)
            w = im.size[0]
            h = im.size[1]
            if w < self.wmin:
                self.wmin = w
                wminfile = i
            if h < self.hmin:
                self.hmin = h
                hminfile = i
        print wminfile, self.wmin
        print hminfile, self.hmin

    def crop(self):
        path = './crop/'
        try:
            if not(os.path.isdir(path)):
                os.makedirs(os.path.join(path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print 'Failed to create directory!!!'
                raise
        for i in self.list:
            im = Image.open(i)
            print 'processing {0}...'.format(i)
            w = im.size[0]
            h = im.size[1]
            wgap = w - self.wmin
            hgap = h - self.hmin
            left = wgap / 2
            upper = 0
            right = left + self.wmin
            lower = self.hmin
            cropped = im.crop((left, upper, right, lower))
            print '{0}-->{1}\n'.format((w,h), cropped.size)
            cropped.save(path + i)


def main():
    path = './'
    ld = Loader(path)
    files = ld()
    handler = ImageHandler(files)
    handler()

if __name__=='__main__':
    sys.exit(main())
