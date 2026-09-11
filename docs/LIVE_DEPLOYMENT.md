# Live StudioNet Deployment

Verified on September 11, 2026 against StudioNet (`chainId 61999`). The deployer was loaded from `.env.build`; the private key is not stored in this repository.

## Canonical corrected deployment

- Contract: `0xcAb44063DF99fBE2eC04a7c923BA1bdED3D662D0`
- Deployment transaction: `0x8940ec223a30e16a251b522d987246796a9143305f719becf561373b8d3840c2`
- Deployment consensus: `MAJORITY_AGREE`
- Deployed schema: `finalize_case(case_id)` has no caller-supplied appeal context.

This deployment contains the appeal lifecycle correction: initial reviews omit appeal context, appeal reviews derive context from stored party-authorized state, and `appeal_count` is bounded to one.

The deployed source was fetched from StudioNet by the GenLayer Project Review Kit and manually compiled and linted successfully. The Review Kit fetch helper reports a relative-path issue when invoking its internal checks, so the fetched artifact was checked directly.

## Live lifecycle test

- Case: `appeal-finality-1788822773143`
- Open transaction: `0xb0a169935ee4efebaf7b1c2e01963083077144ed76d9c7f5e233278c963a0715`
- Submit transaction: `0x3fdcad15c1f7566143f8710c97cafc38b19b1d7b2c1a8fa5743f1ffd9ea268ac`
- Initial finalization transaction: `0x37ad6035f838690e8623e3761a5e96e77fc2f7dbbfcf337cff918d9477c257fd`
- Appeal transaction: finalized with stored `appeal_count: 1` and the authorized reason.
- Appeal finalization transaction: `0x7d649feab29f00fab30aaaaf0ab992248d5fef33a1103693eb4da7d4b64ac0d6`
- Finalization consensus: `MAJORITY_AGREE`; final stored review is `review_number: 2`, `FULFILLED`, `settlement_bps: 10000`.
- Final state: `FINALIZED` and ready for settlement.
- Second-appeal rejection transaction: `0x16516f802bafc036ecf4dcbc590ef7f498333d907dd56c9a40821fec3b6e8a8d`
- Second-appeal result: transaction finalized with `MAJORITY_AGREE`, but contract execution returned `ERROR` as expected for `Appeal limit reached`; state remained `FINALIZED`.

The earlier deployments at `0x970e0c2963A8000CDe6C04948f477aF970F6841B` and `0x28bD13E6937BCdf29eCb370777BDb7202d8E0Dde` are prior revisions. The Explorer submission should use the canonical corrected address above.
