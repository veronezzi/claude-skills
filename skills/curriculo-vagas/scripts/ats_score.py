#!/usr/bin/env python3
"""Calcula score ATS por keyword match entre CV e job description.

Uso:
  python ats_score.py cv.txt job.txt
  python ats_score.py --cv cv.txt --job job.txt
"""
import argparse
import re
import sys
from collections import Counter

STOPWORDS = {
    "de", "da", "do", "das", "dos", "e", "a", "o", "as", "os", "em", "para",
    "com", "por", "que", "um", "uma", "uns", "umas", "no", "na", "nos", "nas",
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "with", "on",
    "at", "by", "is", "are", "was", "were", "be", "been", "being", "as",
}


def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9áéíóúâêôãõç+#.\-]", " ", text)
    toks = [t for t in text.split() if len(t) > 1 and t not in STOPWORDS]
    return toks


def extract_phrases(text, n=2):
    toks = tokenize(text)
    phrases = []
    for i in range(len(toks) - n + 1):
        phrases.append(" ".join(toks[i:i+n]))
    return phrases


def score(cv_text, job_text):
    job_tokens = tokenize(job_text)
    cv_tokens = tokenize(cv_text)
    job_set = set(job_tokens)
    cv_set = set(cv_tokens)

    # keyword match (unigrams)
    matched = job_set & cv_set
    missing = job_set - cv_set
    kw_score = (len(matched) / len(job_set) * 100) if job_set else 0

    # bigram match
    job_bi = set(extract_phrases(job_text))
    cv_bi = set(extract_phrases(cv_text))
    bi_matched = job_bi & cv_bi
    bi_score = (len(bi_matched) / len(job_bi) * 100) if job_bi else 0

    # combined (weighted)
    combined = kw_score * 0.6 + bi_score * 0.4

    # top missing keywords
    job_counts = Counter(job_tokens)
    missing_ranked = sorted(missing, key=lambda w: job_counts[w], reverse=True)[:20]

    return {
        "keyword_score": round(kw_score, 1),
        "bigram_score": round(bi_score, 1),
        "combined": round(combined, 1),
        "matched_count": len(matched),
        "total_job_keywords": len(job_set),
        "missing_top": missing_ranked,
        "matched_sample": sorted(matched)[:20],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cv", nargs="?")
    parser.add_argument("job", nargs="?")
    parser.add_argument("--cv", dest="cvf")
    parser.add_argument("--job", dest="jobf")
    args = parser.parse_args()

    cv_path = args.cvf or args.cv
    job_path = args.jobf or args.job
    if not cv_path or not job_path:
        print("Uso: python ats_score.py cv.txt job.txt", file=sys.stderr)
        sys.exit(1)

    with open(cv_path, encoding="utf-8-sig") as f:
        cv_text = f.read()
    with open(job_path, encoding="utf-8-sig") as f:
        job_text = f.read()

    res = score(cv_text, job_text)
    print(f"Score combinado: {res['combined']}/100")
    print(f"  Keyword match: {res['keyword_score']} ({res['matched_count']}/{res['total_job_keywords']})")
    print(f"  Bigram match:  {res['bigram_score']}")
    print()
    print("Top keywords faltando:")
    for w in res["missing_top"]:
        print(f"  - {w}")
    print()
    print("Sample de keywords encontradas:")
    print("  " + ", ".join(res["matched_sample"]))


if __name__ == "__main__":
    main()
