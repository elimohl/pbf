import sys
import os


class BFException(Exception):
    def __init__(self, error_name, explanation):
        self.error_name = error_name
        self.explanation = explanation

    def __str__(self):
        return 'Brainfuck {} error: {}'.format(self.error_name, self.explanation)


class Node:
    def __init__(self, name):
        self.name = name
        self.childrens = []

    def execute(self, cells, tree):
        if self.name == 'root':
            for node in self.childrens:
                node.execute(cells, tree)
        elif self.name == '>':
            tree.cell_num += 1
            if len(cells) < tree.cell_num + 1:  # cell_num >= 0
                cells.append(0)
        elif self.name == '<':
            tree.cell_num -= 1
            if tree.cell_num < 0:
                raise BFException('execution', 'Trying to move pointer out of boundary.')
        elif self.name == '+':
            cells[tree.cell_num] = (cells[tree.cell_num] + 1) % 256
        elif self.name == '-':
            cells[tree.cell_num] = (cells[tree.cell_num] - 1) % 256
        elif self.name == '.':
            sys.stdout.write(chr(cells[tree.cell_num]))
        elif self.name == ',':
            cells[tree.cell_num] = ord(sys.stdin.read(1))
        elif self.name == '[]':
            while cells[tree.cell_num] != 0:
                for node in self.childrens:
                    node.execute(cells, tree)


class Tree:
    def __init__(self, root):
        self.root = root
        self.cell_num = 0


def parse(root, source):
    while True:
        ch = source.read(1)
        if not ch:
            if root.name != 'root':
                raise BFException('syntax', 'Missing "]".')
            return
        elif ch in ['>', '<', '+', '-', '.', ',']:
            node = Node(ch)
            root.childrens.append(node)
        if ch == '[':
            node = Node('[]')
            root.childrens.append(node)
            parse(node, source)
        elif ch == ']':
            return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: %s file name' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: File  %s was not found!' % sys.argv[1])

    source_file = open(sys.argv[1], 'r')

    try:
        root = Node('root')
        tree = Tree(root)
        parse(root, source_file)

        cells = [0]
        root.execute(cells, tree)
    except BFException as e:
        print e
