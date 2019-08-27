import re

class PlaceholderProcessor:

    def __init__(self):
        self._mod = 'placeholder'
        self._r = re.compile(r"｟[^｟｠]*｠")

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    def preprocess(self, seg):
        placeholders = self._r.findall(seg.src)
        to_sub = {ph: re.sub(' ', '_', ph) for ph in placeholders}
        for placeholder in to_sub:
            seg.src = re.sub(placeholder, to_sub[placeholder], seg.src)

    def preprocess_str(self, str):
        placeholders = self._r.findall(str)
        to_sub = {ph: re.sub(' ', '_', ph) for ph in placeholders}
        for placeholder in to_sub:
            str = re.sub(placeholder, to_sub[placeholder], str)
        return str

    def postprocess(self, seg):
        placeholders = self._r.findall(seg.tgt)
        to_sub = {ph: re.sub('_', ' ', ph) for ph in placeholders}
        for placeholder in to_sub:
            seg.tgt = re.sub(placeholder, to_sub[placeholder], seg.tgt)

    def postprocess_str(self, str):
        placeholders = self._r.findall(str)
        to_sub = {ph: re.sub('_', ' ', ph) for ph in placeholders}
        for placeholder in to_sub:
            str = re.sub(placeholder, to_sub[placeholder], str)
        return str
