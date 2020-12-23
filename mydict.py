#!/usr/bin/python3
import csv, random
class Dictionary:
    def __init__(self, lang1, lang2):
        self.lang = [lang1, lang2]
        self.numentries = 0
        self.vocabulary = []
        self.learningsubset = []
        self.block = []
        self.learned = []

    def add(self, vocable1, vocable2):
        dict = {self.lang[0]: vocable1, self.lang[1] : vocable2}
        self.vocabulary.append(dict)
        self.numentries = self.numentries + 1

    def getblock(self, numentries, offset, numvoc):
        if not numvoc: numvoc = 0
        self.learned.extend(self.block)
        block = []
        blockrange = numvoc
        start = blockrange * offset
        self.learningsubset = self.vocabulary[start:start+blockrange]
        for i in range(numentries):
            voc = random.randint(0, blockrange - 1)
            inblock = self.learningsubset[voc] in block
            learned = self.learningsubset[voc] in self.learned
            optionsleft = len(self.learned) + len(block) < len(self.learningsubset)
            if optionsleft:
                while inblock or learned:
                    voc = random.randint(0, blockrange - 1)
                    inblock = self.learningsubset[voc] in block
                    learned = self.learningsubset[voc] in self.learned
            else:
                print("Nearly all learned! This is the last block.")
                break
            block.append(self.learningsubset[voc])
        self.block = block
        return block

    def replace(self, replace):
        self.learned.append(self.block[replace])
        voc = random.randint(0, len(self.learningsubset) - 1)
        inblock = self.learningsubset[voc] in self.block
        learned = self.learningsubset[voc] in self.learned
        optionsleft = len(self.learned) < len(self.learningsubset)
        while (inblock or learned) and optionsleft:
            voc = random.randint(0, len(self.learningsubset) - 1)
            inblock = self.learningsubset[voc] in self.block
            learned = self.learningsubset[voc] in self.learned
        self.block[replace] = self.learningsubset[voc]
        return self.block

def fromcsv(filename):
    with open(filename, encoding = 'ISO 8859-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        lang1 = header[0]
        lang2 = header[1]
        dict = Dictionary(lang1, lang2)
        for row in list(reader):
            dict.add(row[0], row[1])
        return dict
