from model.learner import Task
from model.pipe import Pipe
from numpy import fromiter, int32

# converts the input array of word id's, the input should be a wordstream, which considers the models #windowsize
# and provides wentBack and wentPast to indicate words prepended and appended that do not belong to the
# designated range in a partial file, which needs to be passed for proper processing

class convertWordIds(Pipe):
    def feed(self, threadid, task):
        def genWords(input, vocab):
            for term in input:
                word = vocab.get(term)
                if word is not None:
                    yield word.index

        wordstream = task.pyparams
        wordidstream = (fromiter(genWords(wordstream, self.model.vocab), dtype=int32), wordstream.wentBack, wordstream.wentPast)
        newtask = Task(priority=1/len(wordidstream))
        newtask.pyparams = wordidstream
        self.addTask(newtask, task)

