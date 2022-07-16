class C_list:
    def __init__(self, lis:list):
        self.lis = lis

    # Sample Method
    def append(self, var):
        self.lis.append(var)

    def remove_duplicate(self):
        res = []
        for i in self.lis:
            if i not in res:
                res.append(i)
        self.lis.clear()
        for i in res:
            self.lis.append(i)

    def clear(self):
        self.lis.clear()


