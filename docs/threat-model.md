# Threat model

The contract defends against fabricated citations, stale or uncommitted submissions, prompt injection in evidence, malformed model output, external-source failure, duplicate finalization, unauthorized delivery, caller-supplied appeal prompt injection, and replayed appeals. URLs are bounded and committed before review; unavailable evidence cannot produce an accepted result. Appeals are party-authorized in storage and bounded to one per case, guaranteeing that a finalized review cannot be reopened indefinitely.
