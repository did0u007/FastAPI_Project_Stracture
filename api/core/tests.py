import time


class Test:
    name = None

    def __init__(self, name=None):
        self.name = name


lst1 = range(10)
lst2 = range(5, 20)
list1 = [Test(str(i)) for i in lst1]
list2 = [Test(str(i)) for i in lst2]
