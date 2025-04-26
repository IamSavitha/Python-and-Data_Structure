class MyList:
    def __init__(self):
        self.items = []
    
    def append(self, item):
        self.items += [item]
    
    def insert(self, index, item):
        self.items = self.items[:index] + [item] + self.items[index:]
    
    def remove(self, item):
        for i in range(len(self.items)):
            if self.items[i] == item:
                self.items = self.items[:i] + self.items[i+1:]
                return
        raise ValueError("Item not found in the list")
    
    def __str__(self):
        return str(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __len__(self):
        return len(self.items)
