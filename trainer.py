#!/usr/bin/python3
import mydict, argparse, sys, random, getpass, datetime

root = "/home/susanne/dev/python-playground/dictionary/"
def main(args):
    path = root + args.file +".csv"
    dict = mydict.fromcsv(path)
    print("Press Enter to start or 's' to stop.\n")
    print("If you learn in blocks, press")
    print("\t 'n' for the next block")
    print("\t 'r' to replace a vocabulary in the current block")
    print("\t 'b' to print the current block")
    block = dict.vocabulary
    if args.blocks:
        offset = -1
        if args.blockoffset:
            #offset = datetime.datetime.today().weekday()
            offset = getoffset(args.numvoc)
        block = dict.getblock(args.blocks, offset, args.numvoc)
        command = input()
        print("Learning block:\n")
        printblock(block)
        command = input()
    voc = 0
    while command != 's':
        if args.blocks and command == "n":
            block = dict.getblock(args.blocks, offset, args.numvoc)
            print("Learning block:\n")
            printblock(block)
            command = input()
        if command in ('n', 's'): continue
        if args.random: bit = random.randint(0,1)
        elif args.other: bit = 1
        else: bit = 0
        #voc = random.randint(0, len(block) - 1)
        print(block[voc].get(dict.lang[bit]), end = "")
        command = input()
        #print("\033[30C\033[1A" + block[voc].get(dict.lang[(bit + 1) % 2]))
        print(block[voc].get(dict.lang[(bit + 1) % 2]))
        command = input()
        if command in ('n', 's'): continue
        if command == 'r':
            block = dict.replace(voc)
            print("\nReplacement:")
            printentry(block[voc])
            continue
        if command == "german": args.random = False
        elif command == "other":
            args.random = False
            args.other = True
        elif command == "b": printblock(block)
        voc = (voc + 1) % len(block)

def getoffset(numvoc):
    if not numvoc: numvoc = 60
    with open(root + "/offset", 'r') as off:
        offset = int(off.read())
    with open(root + "/offset", 'w') as off:
        off.write(str(offset + int(numvoc)))
    return offset

def printblock(dictlist):
    keys = list(dictlist[0].keys())
    for dict in dictlist:
        print(f'{dict.get(keys[0]):20} {dict.get(keys[1])}')

def printentry(dict):
    keys = list(dict.keys())
    print(f'{dict.get(keys[0]):20} {dict.get(keys[1])}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vocabulary trainer.')
    parser.add_argument('-f', '--file',
        help='defines the dictionary file:\n'+
        'it: german-italian words\n'+
        'it-sent: german-italian sentences')
    parser.add_argument('-r', '--random',
        help='mix languages randomly', action="store_true")
    parser.add_argument('-o', '--other',
        help='show other lang first', action="store_true")
    parser.add_argument('-b', '--blocks', type=int,
        help='learn in blocks of the argument size')
    parser.add_argument('-off', '--blockoffset', action="store_true",
        help='start from the block after last session')
    parser.add_argument('-n', '--numvoc', type=int,
        help='number of vocabulary you want to learn')
    args = parser.parse_args()
    main(args)
