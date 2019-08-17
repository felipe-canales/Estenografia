import argparse
import pai_io
import decodifier

parser = argparse.ArgumentParser()

# Arguments
mode = parser.add_mutually_exclusive_group(required = True)

mode.add_argument("--encode", action = 'store_true', help = "encodes text in an image")
mode.add_argument("--decode", action = 'store_true', help = "decodes text from an image")
parser.add_argument("--image", metavar = '<image filename>', required = True,
                    help = "image to be encoded/decoded")
parser.add_argument("--text", metavar = '<text filename>',
                    help = "text to be encoded in an image")
parser.add_argument("--nbits", metavar =  '<N>', type = int,
                    help = "amount of bits (between 1 and 8) used per pixel")

argss = parser.parse_args()

# Encoding
def encode(image_file, text, bits):
    img = pai_io.imread(image_file)
    ext = len(image_file) - image_file[::-1].index('.') - 1

    is_color = len(img.shape) == 3

    dec = decodifier.Decodifier(img, is_color, bits)
    pai_io.imsave(image_file[:ext] + '_out' + image_file[ext:], dec.encode(text.read()))


# Decoding
def decode(image_file):
    img = pai_io.imread(image_file)
    is_color = len(img.shape) == 3
    if is_color:
        nbits = (img[0][0][0] & 7) + 1
    else:
        nbits = (img[0][0] & 7) + 1

    dec = decodifier.Decodifier(img, is_color, nbits)

    print(dec.decode())

# Validation
if argss.encode:
    if argss.text == None or argss.nbits == None:
        print("tarea_1.py: error: the following arguments are required when encoding: --text, --nbits")
        exit()
    elif 0 >= int(argss.nbits) or int(argss.nbits) > 8:
        print("tarea_1.py: error: --nbits must have a value between 1 and 8")
        exit()
    encode(argss.image, open(argss.text, "r"), argss.nbits)
else:
    decode(argss.image)
