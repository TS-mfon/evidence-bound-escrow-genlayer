# EvidenceBoundEscrow

EvidenceBoundEscrow is a reusable GenLayer Intelligent Contract primitive for escrowed work that cannot be settled by a deterministic API: freelance milestones, procurement acceptance, grants, and service-level disputes.

The sponsor locks native value and a criteria/evidence manifest. The respondent submits a delivery commitment. GenLayer validators independently fetch the committed public evidence and compare the substantive decision through `gl.eq_principle.prompt_comparative`. Consensus controls the settlement basis points and the contract executes the resulting payout, not just an explanation.

Each case starts with an appeal-free review prompt. A sponsor or respondent may authorize one stored appeal reason after finalization; the appeal review reads that reason from case state, and no case can be reopened a second time.

Escrow cannot remain locked forever: an unsubmitted case becomes sponsor-refundable after seven days, while a submitted case with unavailable locked evidence requires comparative outage consensus plus a three-day cure window before sponsor recovery. Available evidence remains reviewable and blocks recovery.

## Why GenLayer

Removing GenLayer removes the trust model: no single platform, seller, or centralized AI service can unilaterally decide whether evidence satisfies the locked criteria and release escrow.

## Run

```bash
uvx --from genvm-linter genvm-lint check contracts/evidence_bound_escrow.py
uvx --from genlayer-test pytest -q tests/direct
```

See `docs/consensus.md` and `docs/threat-model.md` for the complete design boundary.

The canonical corrected StudioNet deployment and matching Explorer lifecycle evidence are documented in `docs/LIVE_DEPLOYMENT.md`. Use `0xcAb44063DF99fBE2eC04a7c923BA1bdED3D662D0`; the repository does not contain private keys.
