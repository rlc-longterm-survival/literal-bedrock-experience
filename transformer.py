from sys import argv
import json
from PIL import Image
import os, shutil
from fnmatch import fnmatch

os.chdir(os.path.dirname(__file__))

print('Bedrocky Resource Transformer')
print('Create a literal Minecraft Bedrock Edition experience with ease.')

if(len(argv) < 2):
    print('Usage: transformer <pack_name>')
    exit()

MASK_DIR = './mask/'
ORIGINAL_DIR = './original/'
OUTPUT_DIR = './output/'
# OUTPUT_DIR = 'E:/MC-experimental/.minecraft/versions/1.20.1/resourcepacks/'

pack_name = argv[1]

FROM_PACK = ORIGINAL_DIR + pack_name + '/'
TO_PACK = OUTPUT_DIR + pack_name + '/'

if(not os.path.isdir(FROM_PACK)):
    print(f'Error: Cannot find pack `{pack_name}`. Be sure to put UNZIPPED resources under the `original` folder.')
    exit()

if os.path.exists(TO_PACK):
    shutil.rmtree(TO_PACK)
os.makedirs(TO_PACK, 0o777, True)

if(not os.path.isdir(FROM_PACK + 'assets/')):
    print('Error: No assets found in the pack.')

print('Info: Loading modes exception')
modes_exception = json.load(open('mask/modes-exception.json', encoding='utf-8'))
print('Info: Loading pack.mcmeta')
pack_mcmeta = json.load(open('mask/pack.mcmeta', 'r', encoding='utf-8'))
print('Info: Copying pack.mcmeta')
json.dump(pack_mcmeta, open(TO_PACK + 'pack.mcmeta', 'w', encoding='utf-8'))
print('Info: Loading bedrock.png')
mask_image = Image.open('mask/bedrock.png', 'r').convert('RGBA')
[mask_width, mask_height] = mask_image.size

# ===================================================

def do_image(image: Image.Image, mode: str):
    if mode == 'preserve':
        return
    [width, height] = image.size
    for x in range(width):
        for y in range(height):
            if mode == 'transparent':
                image.putpixel((x, y), tuple([0, 0, 0, 0]))
                continue
            alpha = image.getpixel((x, y))[3]
            mask_pixel = mask_image.getpixel((x % mask_width, y % mask_height))
            if mode == 'opaque':
                if alpha != 0:
                    image.putpixel((x, y), tuple([*mask_pixel[0:3], 255]))
            elif mode == 'white':
                if alpha != 0:
                    image.putpixel((x, y), tuple([255, 255, 255, 255]))
            elif mode == 'full':
                image.putpixel((x, y), tuple([*mask_pixel[0:3], 255]))
            else:
                image.putpixel((x, y), tuple([*mask_pixel[0:3], alpha]))

def determine_mode(path: str):
    mode = 'mask'
    path_segs = path.strip('/').split('/')[1:]
    exception_key = '/'.join(path_segs)
    for key in modes_exception:
        if fnmatch(exception_key, key):
            mode = modes_exception[key]
    return mode

def process_png(path: str, namespace: str, rootpath: str):
    from_png = FROM_PACK + 'assets/' + namespace + '/' + path
    to_png = TO_PACK + 'assets/' + namespace + '/' + path
    mode = determine_mode(path)
    if mode == 'ignore':
        return
    os.makedirs(os.path.dirname(to_png), 0o777, True)
    # 检查 mcmeta 是否存在
    if os.path.exists(from_png + '.mcmeta'):
        open(to_png + '.mcmeta', 'wb').write(open(from_png + '.mcmeta', 'rb').read())
    # 处理图像
    image = Image.open(from_png, 'r').convert("RGBA")
    do_image(image, mode)
    image.save(to_png, 'png')
    image.close()

def traverse(path: str, namespace, rootpath: str):
    if not os.path.isdir(rootpath + path):
        return
    dirlist = os.listdir(rootpath + path)
    for item in dirlist:
        new_path = rootpath + path + item
        if os.path.isdir(new_path):
            traverse(path + item + '/', namespace, rootpath)
        elif item.endswith('.png'):
            process_png(path + item, namespace, rootpath)

def handle_namespace(namespace: str, rootpath: str):
    print('Info: Processing namespace ' + namespace)
    traverse('textures/', namespace, rootpath)

for namespace in os.listdir(FROM_PACK + 'assets/'):
    rootpath = FROM_PACK + 'assets/' + namespace + '/'
    if os.path.isdir(rootpath):
        handle_namespace(namespace, rootpath)
        
print('Info: Applying overrides')

shutil.copytree('overrides/', TO_PACK, dirs_exist_ok=True)

# ===================================================

print('Info: Creating zip archive')
shutil.make_archive('dist/bedrock-experience-' + pack_name, 'zip', TO_PACK)
