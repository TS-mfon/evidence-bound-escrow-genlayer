# Live StudioNet Deployment

Verified on September 7, 2026 against StudioNet (`chainId 61999`). The deployer was loaded from `.env.build`; the private key is not stored in this repository.

## Deployment

- Contract: `0x970e0c2963A8000CDe6C04948f477aF970F6841B`
- Deployment transaction: `0x56b5b490f42aa3395d575424291ceb02ec9669c790638687935e55e8b2b0c0d3`
- Deployment consensus: `MAJORITY_AGREE`

## Resolved case

- Case: `live-resolution-v2-1788755054759`
- Open transaction: `0x968b96f20e40ca88eeaf406ef0075d5754372dfa8ad9e456c7038c9b57dac009`
- Submit transaction: `0xa33e201b23d8bc1f686afa64f2c5bad2404e3e2069694126f57312afeaf34ff7`
- Finalization transaction: `0x9469cf288bd8e9ab43e9a31b07d67652c4d98f4cacf01f430630a247e686a858`
- Finalization consensus: `MAJORITY_AGREE`
- Stored result: `FULFILLED`, `settlement_bps: 10000`
- Settlement transaction: `0x7de90343fe8f663ba75da3f01627628c977e51502f6af6173b4b1bb5c3997910`
- Final state: `SETTLED`
- Settlement accounting: `1000000000000000` wei to respondent, `0` wei refunded to sponsor.

The first deployed revision correctly rejected malformed CLI input and finalized with an execution rollback. It was not treated as a successful case. The prompt/normalization compatibility fix was redeployed as the address above and then passed the complete `OPEN -> SUBMITTED -> FINALIZED -> SETTLED` flow.
