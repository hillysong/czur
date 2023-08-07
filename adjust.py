from PIL import Image
from argparse import ArgumentParser
from loguru import logger
import os, sys, math


def get_image_list(args):
    path = args.path
    files = [f for f in os.listdir(path) if f.startswith('image')]
    return sorted(files)


def get_statistics(images):
    widths, heights = [], []
    for filename in images:
        image = Image.open(filename)
        widths.append(image.size[0])
        heights.append(image.size[1])

    min_w = min(widths)
    min_w_idx = widths.index(min_w)
    logger.info(f'min_w = {min_w}, {images[min_w_idx]}')

    max_w = max(widths)
    max_w_idx = widths.index(max_w)
    logger.info(f'max_w = {max_w}, {images[max_w_idx]}')

    min_h = min(heights)
    min_h_idx = heights.index(min_h)
    logger.info(f'min_h = {min_h}, {images[min_h_idx]}')

    max_h = max(heights)
    max_h_idx = heights.index(max_h)
    logger.info(f'max_h = {max_h}, {images[max_h_idx]}')

    avg_w = sum(widths) / len(widths)
    avg_h = sum(heights) / len(heights)
    logger.info(f'avg_w = {avg_w}')
    logger.info(f'avg_h = {avg_h}')

    return min_w, min_h, avg_w, avg_h


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, default='./')
    args = parser.parse_args()

    for k, v in vars(args).items():
        logger.info(f'PARAMETER | {k} : {v}')
    logger.info('')
    logger.info('')

    return args


def make_result_directory(args):
    path = os.path.join(args.path, 'adjust')
    try:
        if not (os.path.isdir(path)):
            os.makedirs(os.path.join(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            logger.error('Failed to create directory!!!')
            raise


def crop_or_resize_w(files, avg_w, args):
    new_images = []
    for f in files:
        image = Image.open(f)
        w = int(image.size[0])
        h = int(image.size[1])
        avg_w = int(avg_w)

        if w > avg_w:
            diff_w = int(math.floor((w - avg_w) / 2))
            new_image = image.crop((diff_w, 0, avg_w + diff_w, h))
            done = 'cropped'
        else:
            new_image = image.resize((avg_w, h))
            done = 'resized'
        logger.info(f'{f} is w-{done }to ({avg_w}, {h})')
        new_images.append(new_image)
    return new_images


def crop_or_resize_h(images, filenames, avg_h, args):
    assert len(images) == len(filenames)
    path = os.path.join(args.path, 'adjust')
    for image, name in zip(images, filenames):
        w = int(image.size[0])
        h = int(image.size[1])
        avg_h = int(avg_h)

        if h > avg_h:
            diff_h = int(math.floor((h - avg_h) / 2))
            new_image = image.crop((0, diff_h, w, avg_h + diff_h))
            done = 'cropped'
        else:
            new_image = image.resize((w, avg_h))
            done = 'resized'
        logger.info(f'{name} is h-{done} to ({w}, {avg_h})')
        new_image.save(os.path.join(path, name))


def main():
    args = parse_args()
    make_result_directory(args)
    files = get_image_list(args)
    min_w, min_h, avg_w, avg_h = get_statistics(files)
    images = crop_or_resize_w(files, avg_w, args)
    crop_or_resize_h(images, files, avg_h, args)


if __name__ == '__main__':
    sys.exit(main())
