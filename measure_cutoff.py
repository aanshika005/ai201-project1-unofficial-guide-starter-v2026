"""
Milestone 4 helper: measure the two groups of distances.

Runs all five test questions and all five OUT_OF_SCOPE questions through
retrieval only — no model call, so it costs no API quota — and prints the best
(lowest) distance for each. The gap between the two groups is where the
relevance cutoff belongs.

    python measure_cutoff.py
    python measure_cutoff.py --top-k 4

Nothing here is part of the pipeline; it only reads. Delete it when you're done
or keep it as the evidence behind the number you picked.
"""

import argparse

import config
import questions
from store import search


def best(question: str, top_k: int):
    results = search(question, top_k=top_k)
    if not results:
        return None, None
    return results[0].distance, results[0].source


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-k", type=int, default=config.TOP_K)
    args = ap.parse_args()

    print(f"corpus={config.CORPUS}  top_k={args.top_k}  "
          f"current THRESHOLD={config.THRESHOLD}\n")

    print("=" * 78)
    print("IN-CORPUS — questions your documents should answer")
    print("=" * 78)
    in_scope = []
    for q in questions.answered():
        d, src = best(q["question"], args.top_k)
        in_scope.append(d)
        print(f"  {d:.4f}  {src:<34} {q['question'][:46]}")

    print()
    print("=" * 78)
    print("OUT-OF-SCOPE — questions your documents clearly don't cover")
    print("=" * 78)
    out_scope = []
    for q in questions.OUT_OF_SCOPE:
        d, src = best(q, args.top_k)
        out_scope.append(d)
        print(f"  {d:.4f}  {src:<34} {q[:46]}")

    worst_in = max(in_scope)
    best_out = min(out_scope)

    print()
    print("=" * 78)
    print(f"in-corpus    best {min(in_scope):.4f}   worst {worst_in:.4f}")
    print(f"out-of-scope best {best_out:.4f}   worst {max(out_scope):.4f}")
    print("=" * 78)

    if best_out > worst_in:
        print(f"\nGAP: {worst_in:.4f} .. {best_out:.4f}   "
              f"(width {best_out - worst_in:.4f})")
        print(f"Midpoint = {(worst_in + best_out) / 2:.4f}")
        print("\nAny cutoff inside the gap separates the two groups cleanly.")
        print("Nearer the low end refuses more; nearer the high end answers more.")
    else:
        print(f"\nNO CLEAN GAP: worst in-corpus ({worst_in:.4f}) is further away")
        print(f"than the nearest out-of-scope question ({best_out:.4f}).")
        print("No single cutoff separates them. Pick the number that costs you")
        print("least, and say in your README which questions it gets wrong.")


if __name__ == "__main__":
    main()
