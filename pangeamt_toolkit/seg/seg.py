class Seg:
    def __init__(self, src):
        self._src = src
        self._src_raw = src
        self._tgt = None
        self._tgt_raw = None
        self._error = None
        self._src_entities = []
        self._tgt_entities = []
        self._src_case = None
        self._pred_score = 0
        self._attention = None

    def get_src_entities(self):
        return self._src_entities

    def set_src_entities(self, src_entities):
        self._src_entities = src_entities

    src_entities = property(get_src_entities, set_src_entities)


    def get_tgt_entities(self):
        return self._tgt_entities

    def set_tgt_entities(self, tgt_entities):
        self._tgt_entities = tgt_entities

    tgt_entities = property(get_tgt_entities, set_tgt_entities)


    # def preprocess(self, detector):
    #     preprocessed = self._src
    #     if detector is not None:
    #         self._detection = detector.detect(self._src)
    #         preprocessed = self._detection.get_text_with_place_holders()
    #     return preprocessed
    #
    # def postprocess(self):
    #     postprocessed = self.tgt_raw
    #     if self._detection is not None:
    #         # Fist we repace all place holder uuid with associated unicode private char
    #         for replace, match in self._detection.matches.items():
    #             postprocessed = postprocessed.replace(match.id, replace)
    #
    #         # We remove opennmt repetitions
    #         postprocessed = remove_open_nmt_repetition(postprocessed)
    #
    #         # We replace place holder by  appropriate value
    #         for _, match in self._detection.matches.items():
    #             if match.type == Match.TYPE_CHINESE_NUMBER:
    #                 # Hack remove "-" in 4 -brothers
    #                 regex = re.compile(match.replace +  r'(( +)(-)([^0-9]))*')
    #                 replace =  match.translate(self.request.tgt_lang) + r'\2\4'
    #                 postprocessed = re.sub(regex,replace, postprocessed)
    #             elif match.type == Match.TYPE_NUMBER:
    #                 postprocessed= postprocessed.replace(match.replace, match.text)
    #     return postprocessed



    def get_src(self):
        return self._src

    def set_src(self, src):
        self._src = src

    src = property(get_src, set_src)

    def get_src_raw(self):
        return self._src_raw

    src_raw = property(get_src_raw)

    def get_tgt(self):
        return self._tgt

    def set_tgt(self, tgt):
        self._tgt = tgt

    tgt = property(get_tgt, set_tgt)


    def get_tgt_raw(self):
        return self._tgt_raw

    def set_tgt_raw(self, tgt_raw):
        self._tgt_raw = tgt_raw

    tgt_raw = property(get_tgt_raw, set_tgt_raw)


    def get_error(self):
        return self._error

    def set_error(self, error):
        self._error = error
    error = property(get_error, set_error)


    def get_src_case(self):
        return self._src_case

    def set_src_case(self, case):
        self._src_case = case
    src_case = property(get_src_case, set_src_case)


    def get_pred_score(self):
        return self._pred_score

    def set_pred_score(self, pred_score):
        self._pred_score = pred_score
    pred_score = property(get_pred_score, set_pred_score)


    def get_attention(self):
        return self._attention

    def set_attention(self, attention):
        self._attention = attention
    attention = property(get_attention, set_attention)
