import sys
import os

import markovify

if len(sys.argv) != 2:
    print("Gimme files")
    os.exit(1)

with open(sys.argv[1]) as f:
    corpus = f.read()

model = markovify.Text(corpus)

for i in range(1000):
    print(model.make_sentence())
    if i % 5 == 0:
        print('\n')
