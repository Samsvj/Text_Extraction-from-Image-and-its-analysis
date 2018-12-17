#!usr/bin/python 

import pytesseract
from pytesseract import image_to_string
import PIL
from PIL import Image 

img=Image.open('......png')

text=image_to_string(img)
print (text)
