CONF_PATH = '/home/potplus/Desktop/pyrun/mrcnn/data/list_landmarks_inshop.txt'
OUT_PATH = '/home/potplus/Dropbox/linux-sync/cocod'

import os
from PIL import Image
from PIL import ImageDraw


classes = {
    1: 'upper',
    2: 'lower',
    3: 'full'
}


def load_conf():
    with open(CONF_PATH) as f:
        lines = f.readlines()
        lines = lines[2:]
        print('read file ' + CONF_PATH)
        ret = []
        for line in lines:
            line_arr = line.split()
            filepath = line_arr[0]
            cloth_class = int(line_arr[1])
            coords = []
            for i in range(4, len(line_arr), 3):
                coords.append((int(line_arr[i]), int(line_arr[i + 1])))
            ret.append((filepath, cloth_class, coords))

    return ret

def draw_png (conf_lst):
    id = 0
    for line in conf_lst:
        classid = line[1]
        coords = line[2]

        jpg_path = '/home/potplus/Desktop/pyrun/mrcnn/data'
        jpg_path = os.path.join(jpg_path, line[0])

        reorder = []
        if len(coords) == 6:
            reorder = [0,2,4,5,3,1]
        elif len(coords) == 4:
            reorder = [0,1,3,2]
        else:
            reorder = [0,1,3,5,7,6,4,2]

        coords = [coords[i] for i in reorder]

        im = Image.new('L', (256, 256), 1)
        ImageDraw.Draw(im, 'L').polygon(coords, 'white')
        im.save(os.path.join(OUT_PATH,'train', 'annotations',str(id) + '_' + classes[classid] + '_0' + '.png'), 'PNG')

        # save jpg
        im = Image.open(jpg_path)
        im.save(os.path.join(OUT_PATH,'train' ,'shapes_train2019', str(id) + '.jpeg'), 'JPEG')

        id += 1


draw_png(load_conf())