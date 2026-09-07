# EvidenceBoundEscrow

EvidenceBoundEscrow is a reusable GenLayer Intelligent Contract primitive for escrowed work that cannot be settled by a deterministic API: freelance milestones, procurement acceptance, grants, and service-level disputes.

The sponsor locks native value and a criteria/evidence manifest. The respondent submits a delivery commitment. GenLayer validators independently fetch the committed public evidence and compare the substantive decision through `gl.eq_principle.prompt_comparative`. Consensus controls the settlement basis points and the contract executes the resulting payout, not just an explanation.

## Why GenLayer

Removing GenLayer removes the trust model: no single platform, seller, or centralized AI service can unilaterally decide whether evidence satisfies the locked criteria and release escrow.

## Run

```bash
uvx --from genvm-linter genvm-lint check contracts/evidence_bound_escrow.py
uvx --from genlayer-test pytest -q tests/direct
```

See `docs/consensus.md` and `docs/threat-model.md` for the complete design boundary.

The verified StudioNet deployment and completed resolution transactions are documented in `docs/LIVE_DEPLOYMENT.md`. The repository does not contain private keys; live writes require the caller to provide their own signer through local environment configuration.
