# run.py

from PIL import Image as img
import common_lib as clib
import spread_crop as sc

# config
path_in = 'c:\\out\\original\\'
path_out = 'c:\\out\\crop\\'

# get files
clib = clib.CommonLib()
imgs = clib.list_files(path_in)

# run cropping
spread = sc.SpreadCrop(imgs)
spread.set_path_in(path_in)
spread.set_path_out(path_out)
spread.run()
