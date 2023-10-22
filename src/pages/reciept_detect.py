from PIL import Image
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
filename = 'sample.png'
img1 = np.array(Image.open(filename))
text = pytesseract.image_to_string(img1)
print(text)