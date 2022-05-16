class Tree:
    def __init__(self, x=None, parent=None, child=None):
        self.parent = parent
        self.element = x
        self.child = child

    def set_element(self, x: set):
        self.element = x

    def union(self, a: "Tree"):
        self.child = a
        a.parent = self

    def deunion(self):
        self.child = None

    def __contains__(self, item):
        ptr = self
        while ptr is not None:
            if item in ptr.element:
                return True
            ptr = ptr.child
