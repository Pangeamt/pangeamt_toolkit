class AttentionMatrix:
    def __init__(self, src_tokens, tgt_tokens, matrix):
        self._src_tokens = src_tokens
        self._tgt_tokens = tgt_tokens
        self._matrix = matrix

    def get_src_tokens(self):
        return self._src_tokens
    src_tokens = property(get_src_tokens)

    def get_tgt_tokens(self):
        return self._tgt_tokens
    tgt_tokens = property(get_tgt_tokens)

    def get_matrix(self):
        return self._matrix
    matrix = property(get_matrix)

