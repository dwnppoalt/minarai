from fastpunct import FastPunct

class Proofreader:
    def __init__(self) -> None:
        self.fastpunct = FastPunct()
    
    def proofread(self, query):
        return self.fastpunct.punct(query, correct=True)
