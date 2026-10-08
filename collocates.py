import argparse
import os

from qhchina import load_stopwords
from qhchina.analytics.collocations import find_collocates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTENCES_PATH = os.path.join(BASE_DIR, "sentences.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

TOP_N = 20

RUNS = [
    ("window_h5", {"method": "window", "horizon": 5}),
    ("window_h10", {"method": "window", "horizon": 10}),
    ("sentence", {"method": "sentence"}),
]


def load_sentences(path):
    with open(path, encoding="utf-8") as f:
        return [line.split() for line in f if line.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Find collocates for a target word in sentences.txt."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="我",
        help="target word to analyze (default: 我)",
    )
    args = parser.parse_args()
    target_word = args.target

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sentences = load_sentences(SENTENCES_PATH)
    stop_words = load_stopwords("zh_sim")

    filters = {
        "stopwords": stop_words,
        "min_word_length": 2,
        "max_p": 0.05,
    }

    for name, kwargs in RUNS:
        df = find_collocates(
            sentences,
            target_word,
            sort_by="obs_local",
            ascending=False,
            filters=filters,
            **kwargs,
        )
        csv_path = os.path.join(
            OUTPUT_DIR, f"collocates_{target_word}_{name}.csv"
        )
        df.to_csv(csv_path, index=False)

        print(f"\n=== {name} ({kwargs}) -> {csv_path} ===")
        cols = [c for c in ("target", "collocate", "obs_local", "p_value") if c in df.columns]
        print(df[cols].head(TOP_N).to_string(index=False))


if __name__ == "__main__":
    main()
