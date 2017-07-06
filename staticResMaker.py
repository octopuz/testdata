#!/usr/bin/python
# coding=utf-8

import os
import random
import shutil
# import pdb

DICT_OTHER = "./OTHER.dict"
DICT_ENGLISH = "./ENGLISH.dict"
DICT_CHINESE = "./CHINESE.dict"
SIZE_OTHER = os.path.getsize(DICT_OTHER)
SIZE_ENGLISH = os.path.getsize(DICT_ENGLISH)
SIZE_CHINESE = os.path.getsize(DICT_CHINESE)
BIG_RATIO = 0.05        # Big file amount ratio based on all resources
MID_RATIO = 0.30        # Middle file amount ratio based on all resources
SML_RATIO = 0.65        # Small file amount ratio based on all resources
DSTDIR = "/home/zw/test/"


# Define class 'Section' to assemble the specified charactors as a paragraph.
class Section:
    size = 1            # size of the whole section
    lang = 'english'    # digit/symbol/english/chinese/...
    content = ''        # content of the section

    def __init__(self, isize, slang):
        self.size = isize
        self.lang = slang
        if slang == 'chinese':
            iwords = isize / 3
            if (isize % 3) == 0:
                self.content = self.getfill(DICT_CHINESE, SIZE_CHINESE, self.size)
            else:
                self.content = self.getfill(DICT_CHINESE, SIZE_CHINESE, iwords * 3)
        elif self.lang == 'english':
            self.content = self.getfill(DICT_ENGLISH, SIZE_ENGLISH, self.size)
        else:
            self.content = self.getfill(DICT_ENGLISH, SIZE_ENGLISH, self.size)

    def getfill(self, refPath, dstSize, tarSize):
        tmpRead = ''
        refFile = open(refPath, 'r')
        if tarSize <= dstSize:
            return refFile.read(tarSize)
        else:
            # pdb.set_trace()
            cycle = tarSize / dstSize
            itail = tarSize % dstSize
            for i in range(cycle):
                tmpRead += refFile.read(dstSize)
                refFile.seek(0, 0)
            tmpRead += refFile.read(itail)
            return tmpRead
        refFile.close()


# Define class 'ResFile' to assemble content as a txt file.
class ResFile:
    def __init__(self, stype, ssort, spath):
        # 'big' file size scope: 50-100M
        if ssort == 'big':
            self.sort = 'big'
            self.size = random.randint(50000000, 100000000)
            self.paras = random.randint(1, 10) * 10                # total section number
        # 'middle' file size scope: 100k-10M
        elif ssort == 'middle':
            self.sort = 'middle'
            self.size = random.randint(100000, 10000000)
            self.paras = random.randint(1, 10) * 10
        # 'small' file size scope: 2-50K
        else:
            self.sort = 'small'
            self.size = random.randint(2000, 50000)
            self.paras = random.randint(1, 10)
        self.path = spath
        if stype is 'html':
            self.assemblehtml(self.paras, self.size, self.path)
        elif stype is 'xml':
            self.assemblexml(self.paras, self.size, self.path)
        else:
            self.assemble(self.paras, self.size, self.path)

    def assemble(self, iparas, isize, spath):
        # pdb.set_trace()
        itail = isize % iparas
        tmpsize = isize / iparas
        outf = open(spath, 'w')
        for i in range(iparas - 1):
            mylang = random.choice(['english', 'chinese', 'other'])
            mysection = Section(tmpsize, mylang)
            outf.write(mysection.content + '\n')
        if itail == 0:
            tailsect = Section(tmpsize, 'english')
        else:
            tailsect = Section(tmpsize + itail, 'english')
        outf.write(tailsect.content)
        outf.close()

    def assemblehtml(self, iparas, isize, spath):
        itail = isize % iparas
        tmpsize = isize / iparas
        outf = open(spath, 'w')
        outf.write("<html>\n<head>\n  <title>%s</title>\n</head>\n<body>\n" % (spath))
        for i in range(iparas - 1):
            mylang = random.choice(['english', 'chinese', 'other'])
            mysection = Section(tmpsize, mylang)
            outf.write("  <h3>paragraph%s</h3>\n  <p>" % str(i + 1) + mysection.content + "</p>\n")
        if itail == 0:
            tailsect = Section(tmpsize, 'english')
        else:
            tailsect = Section(tmpsize + itail, 'english')
        outf.write("  <h3>paragraph%s</h3>\n  <p>" % (iparas) + tailsect.content + "</p>\n</body>\n</html>")
        outf.close()

    def assemblexml(self, iparas, isize, spath):
        itail = isize % iparas
        tmpsize = isize / iparas
        outf = open(spath, 'w')
        outf.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<document>\n")
        for i in range(iparas - 1):
            mylang = random.choice(['english', 'chinese', 'other'])
            mysection = Section(tmpsize, mylang)
            outf.write("  <section>\n    <head>paragraph%s</head>\n    <body>" % str(i + 1) + mysection.content + "</body>\n  </section>\n")
        if itail == 0:
            tailsect = Section(tmpsize, 'english')
        else:
            tailsect = Section(tmpsize + itail, 'english')
        outf.write("  <section>\n    <head>paragraph%s</head>\n    <body>" % (iparas) + tailsect.content + "</body>\n  </section>\n</document>")
        outf.close()


# Define class 'ResMaker' to create kinds of static resource files.
class ResMaker:
    def __init__(self, itotal, sdir):
        self.dir = sdir
        if itotal <= 100:
            self.batchCreate('small', itotal)
        else:
            big_total = int(round(BIG_RATIO * itotal))
            mid_total = int(round(MID_RATIO * itotal))
            sml_total = int(round(SML_RATIO * itotal))
            self.batchCreate('big', big_total)
            self.batchCreate('middle', mid_total)
            self.batchCreate('small', sml_total)

    def batchCreate(self, ssort, itotal):
        for j in range(itotal):
            mytype = random.choice(['txt', 'html', 'xml'])
            mypath = self.dir + ssort + str(j + 1) + '.' + mytype
            myfile = ResFile(mytype, ssort, mypath)
            print "successfully assemble %d bytes for %s, %d of total %d is finished." % (myfile.size, mypath, (j + 1), itotal)


# Main function is here
if __name__ == '__main__':
    if os.path.exists(DSTDIR):
        shutil.rmtree(DSTDIR)
        os.mkdir(DSTDIR)
    dstfile = ResMaker(100, DSTDIR)
