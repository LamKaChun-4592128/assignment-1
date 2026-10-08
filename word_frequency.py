import os
import re
from collections import Counter

import jieba
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_PATH = os.path.join(BASE_DIR, "data", "novel.txt")
CHART_PATH = os.path.join(BASE_DIR, "word_frequency.png")

CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def load_words(path):
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    return [w for w in jieba.cut(text) if CJK_RE.search(w)]


def main():
    words = load_words(TEXT_PATH)
    counts = Counter(words)

    top10 = counts.most_common(10)
    print("Top 10 most frequent words:")
    for word, count in top10:
        print(f"{word}\t{count}")

    top100 = counts.most_common(100)
    words_100 = [w for w, _ in top100]
    counts_100 = [c for _, c in top100]

    plt.bar(range(len(counts_100)), counts_100)
    plt.xticks([])
    plt.yticks([])
    plt.axis("off")
    plt.savefig(CHART_PATH, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Saved bar chart to {CHART_PATH}")


if __name__ == "__main__":
    main()
