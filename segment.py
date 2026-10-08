import os
import re

import jieba
import opencc
from qhchina import load_stopwords

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_PATH = os.path.join(BASE_DIR, "data", "novel.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "sentences.txt")

SENTENCE_SPLIT_RE = re.compile(r"[。！？]+")
WORD_RE = re.compile(r"\w", re.UNICODE)
MIN_WORDS = 5

WHITELIST = {"他"}

_converter = opencc.OpenCC("t2s")
_stop_words = load_stopwords("zh_sim")


def load_simplified(path):
    with open(path, encoding="utf-8-sig") as f:
        return _converter.convert(f.read())


def tokenize_sentence(sentence):
    return [
        w
        for w in jieba.cut(sentence)
        if WORD_RE.search(w) and (w in WHITELIST or w not in _stop_words)
    ]


def main():
    text = load_simplified(TEXT_PATH)

    sentences = []
    for chunk in SENTENCE_SPLIT_RE.split(text):
        sentence = chunk.strip()
        if not sentence:
            continue
        words = tokenize_sentence(sentence)
        if len(words) >= MIN_WORDS:
            sentences.append(" ".join(words))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sentences))
        if sentences:
            f.write("\n")

    print(f"Wrote {len(sentences)} sentences to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
