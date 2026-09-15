# Live StudioNet Deployment

Verified on September 15, 2026 against StudioNet (`chainId 61999`). The deployer was loaded from `.env.build`; the private key is not stored in this repository.

## Canonical recovery-enabled deployment

- Contract: `0x02408B2f3037993aAc7a1220E3c5F9D458a19196`
- Deployment transaction: `0x024d438848272ddeb12f42ef962dfe20bdf0ed74ea01644fcf36354efd8a7a87`
- Deployment consensus: `MAJORITY_AGREE`
- Explorer: `https://explorer-studio.genlayer.com/address/0x02408B2f3037993aAc7a1220E3c5F9D458a19196`
- Deployed schema: `finalize_case(case_id)` and `recover_case(case_id)` take only the case ID; `appeal_case(case_id, reason)` stores the authorized appeal reason.

This deployment contains the complete lifecycle safeguards: initial reviews omit appeal context, appeal reviews derive context from stored party-authorized state, `appeal_count` is bounded to one, and stalled cases have bounded recovery paths.

## Recovery guarantees

- `OPEN`: only the sponsor can recover, and only after the seven-day submission deadline; the full escrow returns to the sponsor.
- `SUBMITTED`: recovery is blocked while locked evidence is available. If comparative consensus confirms an outage, the first observation starts a three-day cure window; a later confirmation must still include an originally unavailable URL before sponsor recovery.
- `APPEALED`: after the three-day appeal deadline, the prior finalized review is restored and settled through the normal payout path; the appeal cannot strand funds.
- `FINALIZED`, `SETTLED`, and `RECOVERED`: terminal or settlement-controlled states cannot be reopened or recovered again.
- Recovery is callable only by the sponsor or respondent, while payout authorization remains enforced by the stored sponsor/recipient state.

The deployed source was fetched from StudioNet by the GenLayer Project Review Kit and manually compiled and linted successfully. The Review Kit fetch helper reports a relative-path issue when invoking its internal checks, so the fetched artifact was checked directly.

The fetched source matches `contracts/evidence_bound_escrow.py` byte-for-byte. The schema exposes 9 methods: 3 views and 6 writes, including `recover_case(case_id)`.

## Live lifecycle test

- Case: `canonical-finality-1789351238490`
- Open transaction: `0x8d1f79aaa7f115429273284bc4f026b42f7f074bf90bde47c96b119ca156148c`
- Submit transaction: `0xf8b8f4e34c68648bf2994a3907dea5f9da790f54ac0719cbb3223d894dad789c`
- Initial finalization transaction: `0x8a01eb5db6a32a4b3ad013f3d5a843b7b6c565bea0f3fc93fba25d7fea8ecd3f`
- Appeal transaction: `0x15de5fc3b3de464f65ead0f176270f55e0be3cd9c3914a63fbcc225f4c26412b`; finalized with stored `appeal_count: 1` and the authorized reason.
- Appeal finalization transaction: `0x5b27ef3d929393cceb945c01cf9d62d902bd6279d2123ff857cd17a9bee5c459`
- Finalization consensus: `MAJORITY_AGREE`; final stored review is `review_number: 2`, `FULFILLED`, `settlement_bps: 10000`.
- Final state: `FINALIZED` and ready for settlement.
- Second-appeal rejection transaction: `0xe660be39351db645030cf855be23a6bce4d34aa057b09e32c671092da60a6e02`
- Second-appeal result: transaction finalized with `MAJORITY_AGREE`, but contract execution returned `ERROR` as expected for `Appeal limit reached`; state remained `FINALIZED`.

The deadline-based recovery branches are covered by the 11 direct VM tests in `tests/direct/test_contract.py`. They are not represented as live transactions here because exercising the seven-day submission and three-day evidence-cure deadlines on StudioNet would require waiting those real durations; no recovery transaction is claimed without an actual live execution.
