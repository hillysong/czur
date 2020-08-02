from PIL import Image
#import Image
import os, sys, math

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
        self.path = './adjust/'

    def __call__(self):
        #self.smallest()
        #self.cover()
        self.reference()
        cropped = self.cropY()
        self.adjustX(cropped)

    def reference(self):
        cover_page = Image.open(self.list[0])
        self.wmin = cover_page.size[0]
        hmin_file = ''
        hsum = 0
        for f in self.list:
            im = Image.open(f)
            hsum = hsum + im.size[1]
        self.hmin = hsum / len(self.list)
        print('reference height = {}'.format(self.hmin))

    def adjustX(self, images):
        cover = Image.open(self.list[0])
        basis = cover.size[0]
        try:
            if not(os.path.isdir(self.path)):
                os.makedirs(os.path.join(self.path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print('Failed to create directory!!!')
                raise
        for i in images:
            print('Adjusting {0}...'.format(i.filename))
            w = i.size[0]
            h = i.size[1]
            if w > basis:
                wgap = w - basis
                left = math.floor(wgap / 2)
                layer = i.crop((left, 0, left + basis, h))
                print('crop:{0}-->{1}\n'.format((w,h), layer.size))
            else:
                size = (basis, h)
                #r, g, b = i.getpixel((w / 2, 10))
                #print('(r, g, b) = {}, {}, {}'.format(r, g, b))
                #layer = Image.new('RGB', size, (r, g, b))
                layer = Image.new('RGB', size, (255, 255, 255))
                layer.paste(i, tuple(map(lambda x:math.floor((x[0] - x[1]) / 2), zip(size, i.size))))
                print('paste:{0}-->{1}\n'.format((w,h), layer.size))
            layer.save(self.path + i.filename)
            #layer.save(self.path + i.filename, dpi=(250,250))

    def cropY(self):
        res = list()
        for f in self.list:
            im = Image.open(f)
            w = im.size[0]
            h = im.size[1]
            print('Cropping {0}...'.format(f))
            cropped = im.crop((0, 0, w, self.hmin))
            cropped.filename = f
            print('{0}-->{1}\n'.format((w,h), cropped.size))
            res.append(cropped)
        return res


def main():
    path = './'
    ld = Loader(path)
    files = ld()
    handler = ImageHandler(files)
    handler()

if __name__=='__main__':
    sys.exit(main())
