# spread_crop.py

from PIL import Image as img


class SpreadCrop:
    def __init__(self, images):
        self.path_in = 'c:\\out\\original\\'
        self.path_out = 'c:\\out\\crop\\'
        self.images = images
        self.image = '' # actual image reference

    def run(self):
        for item in self.images:
            self.image = img.open(self.path_in + item)
            self.crop_image()

    def crop_image(self):
        print('eredeti oldalpár:', self.image.filename, '(', self.image.width, 'x', self.image.height, ')')
        w = self.image.width
        h = self.image.height
        w2 = abs(w / 2)
        filename = self.image.filename.replace(self.path_in, '')
        filename_left = filename.replace('.jpg', '_1.jpg')
        filename_right = filename.replace('.jpg', '_2.jpg')

        # crop(left, upper, right, lower)
        # new images
        img_left = self.image.crop((0, 0, w2, h))
        img_right = self.image.crop((w2, 0, w, h))

        # saving
        img_left.save(self.path_out + filename_left)
        img_right.save(self.path_out + filename_right)

        print('bal oldal - mentve:', self.path_out + filename_left, '(', img_left.width, 'x', img_left.height, ')')
        print('jobb oldal - mentve:', self.path_out + filename_right, '(', img_right.width, 'x', img_right.height, ')')
        print('----------------------------------------------------------------')

    def set_path_in(self, path_in):
        self.path_in = path_in

    def set_path_out(self, path_out):
        self.path_out = path_out

#end