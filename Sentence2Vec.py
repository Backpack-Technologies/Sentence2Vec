# -*- coding: utf-8 -*-

import gensim
import smart_open
import multiprocessing
from gensim.models.callbacks import CallbackAny2Vec


cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="iso-8859-1") as f:
        loop = 0
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

            loop += 1
            if loop % 1000 == 0:
                print(loop)

            if loop == 10000000:
                break

model = None
corpus = None


def get_result(st):
    inferred_vector = model.infer_vector(st)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    # Compare and print the most/median/least similar documents from the train corpus
    #     print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(corpus[sims[index][0]].words)))


def _start_shell(local_ns=None):
    # An interactive shell is useful for debugging/development.
    import IPython
    user_ns = {}
    if local_ns:
        user_ns.update(local_ns)
    user_ns.update(globals())
    IPython.start_ipython(argv=[], user_ns=user_ns)


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1

    def on_train_begin(self, model):
        print("train started")

    def on_train_end(self, model):
        print("train ended")


def main():
    global model
    global corpus
    corpus = list(read_corpus("data/data.txt"))
    print("Started 1")
    model = gensim.models.doc2vec.Doc2Vec(corpus, vector_size=400, window=100, hs=1, dm=1, min_count=2, epochs=10,
                                          workers=cores, alpha=0.016, min_alpha=0.00001, callbacks=[EpochLogger()])
    # print("Started 2")
    # model.build_vocab(corpus)
    print("Started 3")
    model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs, callbacks=[EpochLogger()])
    print("Started 4")
    model.save("data/doc2vec2.model")

    _start_shell(locals())


if __name__ == "__main__":
    print(cores)
    print(gensim.models.doc2vec.FAST_VERSION)
    main()
