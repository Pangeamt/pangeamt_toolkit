class OnmtxTranslation:
    def __init__(self, src, src_raw, tgt, attn, pred_score):
        self.src = src
        self.src_raw = src_raw
        self.tgt = tgt
        self.attn = attn
        self.pred_score = pred_score

