import random
import pickle
import sys
import os


class Markov:
    def __init__(self, n, p, seed):
        self.n = n
        self.p = p
        self.seed = seed
        self.data = {}

    def train(self, training_data):
        prev = ()
        for token in training_data:
            for pprev in [prev[i:] for i in range(len(prev) + 1)]:
                if not pprev in self.data:
                    self.data[pprev] = []

                self.data[pprev].append(token)

            prev += (token,)
            if len(prev) > self.n:
                prev = prev[1:]

    def load(self, filename):
        with open(os.path.expanduser(filename), "rb") as f:
            try:
                n, self.data = pickle.load(f)

                if self.n > n:
                    print("warning: changing n value to", n)
                    self.n = n
            except:
                print("Loading data file failed!")
                sys.exit(2)

    def dump(self):
        return pickle.dumps((self.n, self.data))

    def __iter__(self):
        random.seed(self.seed)
        self.prev = ()
        return self

    def __next__(self):
        if self.prev == () or random.random() < self.p:
            next = random.choice(self.data[()])
        else:
            try:
                next = random.choice(self.data[self.prev])
            except:
                self.prev = ()
                next = random.choice(self.data[self.prev])

        self.prev += (next,)
        if len(self.prev) > self.n:
            self.prev = self.prev[1:]

        return next
