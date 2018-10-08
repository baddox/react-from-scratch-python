import itertools

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
WARNING = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def color(code, string):
    return code + BOLD + string + ENDC


def indent(level, string):
    prefix = "  " * level
    return prefix + str(string)


class Node:
    def __init__(self, tag, data, children, added=False, removed=False):
        self.tag = tag
        self.data = str(data)
        self.children = children
        self.added = added
        self.removed = removed

    def __str__(self):
        s = "<{} {}>".format(self.tag, self.data)
        return s

    def debug(self, level=0, ancestor_added=False, ancestor_removed=False):
        added = self.added or ancestor_added
        removed = self.removed or ancestor_removed
        s = indent(level, self)
        if added:
            s = color(GREEN, s)
        if removed:
            s = color(RED, s)
        print(s)
        for node in self.children:
            node.debug(
                level + 1, ancestor_added=added, ancestor_removed=removed
            )

    def equals(self, other):
        return self.tag == other.tag and self.data == other.data

    def diff(self, previous):
        # if self.equals(previous):
        #     return Node("{} NO CHANGE".format(self.tag), self.data, [])
        if self.tag != previous.tag:
            return Node(self.tag, self.data, self.children, added=True)

        data = self.data
        if self.data != previous.data:
            data = "{} => {}".format(
                color(RED, previous.data), color(GREEN, self.data)
            )
        children = []
        for child, previous_child in itertools.zip_longest(
            self.children, previous.children
        ):
            if child and not previous_child:
                child_diff = Node(
                    child.tag, child.data, child.children, added=True
                )
            elif previous_child and not child:
                child_diff = Node(
                    previous_child.tag,
                    previous_child.data,
                    previous_child.children,
                    removed=True,
                )
            else:
                child_diff = child.diff(previous_child)
            children.append(child_diff)

        return Node(self.tag, data, children)


def build_node(node):
    if isinstance(node, tuple):
        tag, data, child_nodes = node
        children = [build_node(child_node) for child_node in child_nodes]
        return Node(tag, data, children)
    else:
        return Node("span", node, [])


tree1 = (
    "div",
    0,
    [
        1,
        ("div", 2, [21, 22, 23, 24, 25, 26]),
        3,
        4,
        ("link", 100, [110, 120, ("image", 130, [131, 132])]),
        200,
    ],
)

# data changed
tree2 = (
    "div",
    999,
    [
        1,
        ("div", 222, [21, 22, 23, 24, 25, 26]),
        3,
        4,
        ("link", 100, [110, 120, ("image", 130, [131, 132])]),
        200,
    ],
)

# tag changed
tree3 = (
    "div",
    0,
    [
        1,
        ("p", 2, [21, 22, 23, 24, 25, 26]),
        3,
        4,
        ("link", 100, [110, 120, ("image", 130, [131, 132])]),
        200,
    ],
)

# children added and removed
tree3 = (
    "div",
    0,
    [
        1,
        ("div", 2, [21, 22, 23, 24, 25, 26, 27, 28]),
        3,
        4,
        ("link", 100, [110, 120, ("image", 130, [132])]),
        200,
    ],
)


trees = [tree1, tree2, tree3]

base_node = build_node(tree1)

for tree in trees[1:]:
    node = build_node(tree)
    node.debug()
    print()
    print("Diff:")
    print()
    diff = node.diff(base_node)
    diff.debug()
    print()
    print("===========================")
    print()
