import argparse
import gzip
from pathlib import Path


def smart_open(file):
    if Path(file).suffix == '.gz':
        return gzip.open(file, 'rt')
    else:
        return open(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='Input corpus')
    parser.add_argument('--other', type=str, required=True, help='Corpus for which OOV rate is calculated on')
    args = parser.parse_args()

    with smart_open(args.input) as corpus, smart_open(args.other) as other:
        # input corpus
        voc_input = set()
        for line in corpus:
            words = line.split()
            voc_input.update(words)

        # other corpus
        total_words_other = 0
        oov_running_words = 0
        voc_other = set()
        for line in other:
            words = line.split()
            voc_other.update(words)
            total_words_other += len(words)

            # get OOVs on running words
            for w in words:
                if w not in voc_input:
                    oov_running_words += 1

        # OOVs on vocabulary
        oov_voc = 0
        for w in voc_other:
            if w not in voc_input:
                oov_voc += 1

    print("OOVs on running words: {} / {} = {}".format(oov_running_words, total_words_other,
                                                       oov_running_words / total_words_other))
    print("OOVs on vocabulary: {} / {} = {}".format(oov_voc, len(voc_other),
                                                    oov_voc/len(voc_other)))
