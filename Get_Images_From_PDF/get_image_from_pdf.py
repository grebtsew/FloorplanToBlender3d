import fitz
import cv2

import numpy as np

#pip install minecart
import minecart

pdffile = open('ivar_planlosningar.pdf', 'rb')
doc = minecart.Document(pdffile)

page = doc.get_page(0) # getting a single page

#iterating through all pages
for page in doc.iter_pages():
    im = page.images[0].as_pil()  # requires pillow
    display(im)

'''
https://stackoverflow.com/questions/53059007/python-opencv
'''
def pix2np(pix):
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    im = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
    return im


'''
doc = fitz.open("ivar_planlosningar.pdf")
for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]

        pix = fitz.Pixmap(doc, xref)
        try:

            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None
        except:
            pass

'''


'''
https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
import PyPDF2

from PIL import Image

if __name__ == '__main__':
    input1 = PyPDF2.PdfFileReader(open("ivar_planlosningar.pdf", "rb"))
    page0 = input1.getPage(0)
    xObject = page0['/Resources']['/XObject'].getObject()


    for obj in xObject:
        try:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"


                print("got here")

                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    img.save(obj[1:] + ".png")
                elif xObject[obj]['/Filter'] == '/DCTDecode':
                    img = open(obj[1:] + ".jpg", "wb")
                    img.write(data)
                    img.close()
                elif xObject[obj]['/Filter'] == '/JPXDecode':
                    img = open(obj[1:] + ".jp2", "wb")
                    img.write(data)
                    img.close()
        except:
            print("error")
'''
