import sys

'''
JPG_implementation
Retreive jpg images from pdf files
'''

with open('ivar_planlosningar.pdf',"rb") as file:
    file.seek(0)
    pdf = file.read()

startmark = b"\xff\xd8"
startfix = 0
endmark = b"\xff\xd9"
endfix = 2
i = 0

njpg = 0
while True:
    istream = pdf.find(b"stream", i)
    if istream < 0:
        break
    istart = pdf.find(startmark, istream, istream + 20)
    if istart < 0:
        i = istream + 20
        continue
    iend = pdf.find(b"endstream", istart)
    if iend < 0:
        raise Exception("Didn't find end of stream!")
    iend = pdf.find(endmark, iend - 20)
    if iend < 0:
        raise Exception("Didn't find end of JPG!")

    istart += startfix
    iend += endfix
    print("JPG %d from %d to %d" % (njpg, istart, iend))
    jpg = pdf[istart:iend]
    with open("jpg%d.jpg" % njpg, "wb") as jpgfile:
        jpgfile.write(jpg)

    njpg += 1
    i = iend
