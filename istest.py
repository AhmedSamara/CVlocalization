
class field:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class obj:
    def __init__(self, a, b):
        self.a = a
        self.b = b

f = field(5,6)

a = obj(f,2)


alist = [a]
copylist = list(alist)


b = copylist[0]

print a is b
