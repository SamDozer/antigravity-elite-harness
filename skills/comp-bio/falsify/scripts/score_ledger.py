#!/usr/bin/env python3
"""Computes deterministic Brier scores and Bayesian posterior probabilities for hypothesis falsification."""
import argparse
import math
import sys

def main():
    parser = argparse.ArgumentParser(description="Score falsification hypothesis predictions.")
    parser.add_argument("--prior", type=float, required=True, help="Prior probability P(H) in (0, 1)")
    parser.add_argument("--likelihood-ratio", type=float, required=True, help="Bayes factor P(E|H) / P(E|~H)")
    parser.add_argument("--outcome", type=int, choices=[0, 1], default=None, help="Optional realized outcome (0 or 1) for Brier score")
    args = parser.parse_args()

    if not (0.0 < args.prior < 1.0):
        print("[FAIL] Prior probability must be strictly between 0 and 1.")
        sys.exit(1)
    if args.likelihood_ratio <= 0:
        print("[FAIL] Likelihood ratio must be positive.")
        sys.exit(1)

    prior_odds = args.prior / (1.0 - args.prior)
    post_odds = prior_odds * args.likelihood_ratio
    posterior = post_odds / (1.0 + post_odds)

    msg = f"[PASS] Prior: {args.prior:.4f} | LR: {args.likelihood_ratio:.4f} | Posterior: {posterior:.4f}"
    if args.outcome is not None:
        brier = (posterior - args.outcome) ** 2
        msg += f" | Brier Score: {brier:.4f}"
    print(msg)

if __name__ == "__main__":
    main()
