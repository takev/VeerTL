
class LoopContext (object):
    def __init__(self, i, value=None, length=None, outer=None):
        self.i = i
        self.value = value
        self.outer = outer
        self.length = length
        self.first = (i == 0)

        if length is not None:
            self.last = (i == length - 1)
        else:
            self.last = False

