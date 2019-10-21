class Translation:
    def __init__(self, src, tgt, attention_matrix, score):
        self.src = src
        self.tgt = tgt
        self.attention_matrix =  attention_matrix
        self.score = score
