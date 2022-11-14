class MyTest:
    ai = 0

    def __init__(self, val):
        self.ai = val

    def getAi(self):
        self.ai += 0.1
        return (self.ai)
