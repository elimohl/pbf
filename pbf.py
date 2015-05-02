import sys
import os


if len(sys.argv) < 2:
    sys.exit('Usage: %s file name' % sys.argv[0])

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: File  %s was not found!' % sys.argv[1])

source_file = open(sys.argv[1], 'r')


class Node:
    def __init__(self, ch):
        self.ch = ch
        self.childrens = []


def parse(root):
    while True:
        ch = source_file.read(1)
        if not ch and root.ch != '':
            raise Exception('SYNTAX ERROR: Missing "]".')
        elif ch in ['+', '-', ',', '.', '>', '<', '[', ']']:
            node = Node(ch)
            root.childrens.append(node)
        if ch == '[':
            parse(node)
        elif ch == ']':
            return

root = Node('')
parse(root)
