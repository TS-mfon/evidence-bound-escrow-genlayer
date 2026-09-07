# Consensus design

The leader and validators fetch every locked URL themselves. The comparative principle requires exact agreement on `verdict`, each criterion `decision`, `settlement_bps`, and the hash of fetched evidence. Explanations can differ only in wording. The contract independently enforces criterion weights, citation membership, settlement math, bounds, and state transitions. Every review is retained by sequence number; only the latest finalized review can be settled, and settlement transfers the agreed share to the respondent and refunds the remainder to the sponsor.
