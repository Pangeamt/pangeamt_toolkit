from __future__ import print_function
from onmt.translate.translator import Translator as _Translator
import onmt.model_builder
import onmt.translate.beam
from onmt.translate import TranslationBuilder as _TransBuilder
import onmt.inputters as inputters
import onmt.decoders.ensemble
from pangeamt_toolkit.pangeanmt.onmtx_translation import OnmtxTranslation

class OnmtxTranslator(_Translator):

    def translate(
            self,
            src,
            with_attn=True,
            batch_size=None,
            phrase_table=""):

        src_dir=None

        attn_debug = False
        if with_attn:
            attn_debug = True

        if batch_size is None:
            raise ValueError("batch_size must be set")

        data = inputters.Dataset(
            self.fields,
            readers=([self.src_reader]),
            data=[("src", src)],
            dirs=[src_dir],
            sort_key=inputters.str2sortkey[self.data_type],
            filter_pred=self._filter_pred
        )

        data_iter = inputters.OrderedIterator(
            dataset=data,
            device=self._dev,
            batch_size=batch_size,
            train=False,
            sort=False,
            sort_within_batch=False,
            shuffle=False
        )

        # Translate
        xlation_builder = _TransBuilder(
            data, self.fields, self.n_best, self.replace_unk, None,
            self.phrase_table
        )

        results = []
        for batch in data_iter:

            batch_data = self.translate_batch(
                batch, data.src_vocabs, attn_debug
            )
            translations = xlation_builder.from_batch(batch_data)
            for translation in translations:
                simple_translation = OnmtxTranslation(
                    translation.src,
                    translation.src_raw,
                    translation.pred_sents[0],
                    translation.attns[0],
                    translation.pred_scores[0]
                )
                results.append(simple_translation)
        return results
