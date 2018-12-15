#!usr/bin/python 

import pytesseract
from pytesseract import image_to_string
import PIL
from PIL import Image 

img=Image.open('/home/samiksha/Pictures/Backpropagation.png')

text=image_to_string(img)
print (text)