#!/usr/bin/env bash
set -euo pipefail
uvx --from genvm-linter genvm-lint check contracts/evidence_bound_escrow.py
uvx --from genlayer-test pytest -q tests/direct
