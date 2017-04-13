from intent import Intent
from collections import OrderedDict

# Basic Pipeline
# (TODO): Add basic LRU like features to find then most used intent in first few tests
class Pipeline(object):
    def __init__(self):
        self._pipeline = OrderedDict();
        self.

    def hook(self, key, intent):
        if type(intent) is Intent:
            self._pipeline[key] = {
                "instance": intent,
                "parsed": [] # for future, if we want to lookup which commands it parsed earlier..
            }
        else:
            raise AttributeError("Invalid Intent")

    def unhook(self, key):
        intent = self._pipeline[key]
        del self._pipeline[key]
        return intent

    def findIntent(self, input): # returns the the intents which test positive in the pipeline to be executed!
        intents = []
        for key, intent in self._pipeline:
            if intent["instance"].test(input):
        return intents


