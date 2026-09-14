# Live StudioNet Deployment

Verified on September 14, 2026 against StudioNet (`chainId 61999`). The deployer was loaded from `.env.build`; the private key is not stored in this repository.

## Canonical corrected deployment

- Contract: `0xcAb44063DF99fBE2eC04a7c923BA1bdED3D662D0`
- Deployment transaction: `0x8940ec223a30e16a251b522d987246796a9143305f719becf561373b8d3840c2`
- Deployment consensus: `MAJORITY_AGREE`
- Explorer: `https://explorer-studio.genlayer.com/address/0xcAb44063DF99fBE2eC04a7c923BA1bdED3D662D0`
- Deployed schema: `finalize_case(case_id)` has no caller-supplied appeal context.

This deployment contains the appeal lifecycle correction: initial reviews omit appeal context, appeal reviews derive context from stored party-authorized state, and `appeal_count` is bounded to one.

The deployed source was fetched from StudioNet by the GenLayer Project Review Kit and manually compiled and linted successfully. The Review Kit fetch helper reports a relative-path issue when invoking its internal checks, so the fetched artifact was checked directly.

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
