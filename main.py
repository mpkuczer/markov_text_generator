import string
import random

class Markov(object):
    def __init__(self, filename):
        with open(f'./lib/{filename}.txt') as f:
            self.corpus = f.read()
        self.suffix_map = {}

    def generate_text(self, order=2, length=50, plaintext=True, no_digits=True):
        self.__prepare_corpus(plaintext, no_digits)
        self.__analyze(order)

        if not plaintext:
          while True:
              start_index = random.randrange(len(self.corpus))
              if self.corpus[start_index].istitle():
                  break
        else:
            start_index = random.randrange(len(self.corpus))

        container = self.corpus[start_index:start_index+order]
        prefix = tuple(self.corpus[start_index:start_index+order])

        for _i in range(length):
            suffix = random.choice(self.suffix_map[prefix])
            container.append(suffix)
            prefix = prefix[1:] + (suffix,)

        out = " ".join(container)
        return out

    def __prepare_corpus(self, plaintext, no_digits):
        self.corpus = self.corpus.replace("-", " ").replace("â€ť", '"').replace("â€ś", '"').replace("â€™", "'").split()
        # Replacing hyphens with whitespace.
        # These characters are quotation marks and apostrophes missing from the string.punctuation object.
        
        stripped_corpus = map(lambda w : self.__strip_word(w, plaintext, no_digits), self.corpus)
        empty_strings_removed = filter(lambda w : w != "", stripped_corpus)

        self.corpus = list(empty_strings_removed)

    def __analyze(self, order):
        for i in range(len(self.corpus) - order):
            prefix = tuple(self.corpus[i:i+order])
            self.suffix_map.setdefault(prefix, []).append(self.corpus[i+order])
        
    @staticmethod
    def __strip_word(word, plaintext, no_digits):
        if no_digits:
            word = word.strip(string.digits)
        if plaintext:
            word = word.strip(string.whitespace + string.punctuation).lower()
        return word

if __name__ == "__main__":

    m = Markov('eugene_onegin')
    print(m.generate_text(3, 100, False, True))
    



