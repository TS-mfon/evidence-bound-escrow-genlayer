# Live StudioNet Deployment

Verified on September 7, 2026 against StudioNet (`chainId 61999`). The deployer was loaded from `.env.build`; the private key is not stored in this repository.

## Corrected deployment

- Contract: `0x28bD13E6937BCdf29eCb370777BDb7202d8E0Dde`
- Deployment transaction: `0x484ca656c1e953fa8740bcef966647597e43dd012c347160e048678c9a3d79c3`
- Deployment consensus: `MAJORITY_AGREE`
- Deployed schema: `finalize_case(case_id)` has no caller-supplied appeal context.

This deployment contains the appeal lifecycle correction: initial reviews omit appeal context, appeal reviews derive context from stored party-authorized state, and `appeal_count` is bounded to one.

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

The earlier deployment at `0x970e0c2963A8000CDe6C04948f477aF970F6841B` remains a prior revision. New integrations should use the corrected address above.
