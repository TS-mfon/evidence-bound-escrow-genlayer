import json

CONTRACT = "contracts/evidence_bound_escrow.py"
CRITERIA = json.dumps([{"id": "docs", "statement": "Documentation is published", "weight": 100}])
URLS = json.dumps(["https://example.com/delivery"])


def deploy(direct_deploy, direct_alice):
    return direct_deploy(CONTRACT)


def fund(direct_vm):
    direct_vm.value = 1_000_000


def test_open_and_submit(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-1", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    direct_vm.sender = direct_bob
    result = contract.submit_delivery("case-1", "docs are live", "0x" + __import__("hashlib").sha256(b"docs are live").hexdigest())
    assert result["submission"]["delivery_hash"].startswith("0x")
    assert contract.get_status("case-1") == "SUBMITTED"


def test_rejects_bad_weights(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    fund(direct_vm)
    with direct_vm.expect_revert("Criteria weights must total 100"):
        contract.open_case("bad", direct_bob, json.dumps([{"id": "x", "statement": "x", "weight": 50}]), URLS, "x")


def test_only_respondent_can_submit(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-2", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    with direct_vm.expect_revert("Delivery not authorized"):
        contract.submit_delivery("case-2", "fake", "0x" + __import__("hashlib").sha256(b"fake").hexdigest())


def test_cannot_finalize_without_submission(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-3", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    with direct_vm.expect_revert("Case is not reviewable"):
        contract.finalize_case("case-3")


def test_consensus_finalization_records_payout_and_history(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-4", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    direct_vm.sender = direct_bob
    contract.submit_delivery("case-4", "docs are live", "0x" + __import__("hashlib").sha256(b"docs are live").hexdigest())
    direct_vm.mock_web(r"https://example\.com/delivery", {"status": 200, "body": "The required documentation is public."})
    direct_vm.mock_llm(r".*escrow delivery.*", json.dumps({"verdict": "FULFILLED", "settlement_bps": 10000, "findings": [{"criterion_id": "docs", "decision": "PASS", "citations": ["https://example.com/delivery"], "reason": "Published."}], "summary": "Complete."}))
    result = contract.finalize_case("case-4")
    assert result["result"]["verdict"] == "FULFILLED"
    assert contract.get_review("case-4", 1)["settlement_bps"] == 10000


def test_live_model_aliases_are_normalized(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-alias", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    direct_vm.sender = direct_bob
    contract.submit_delivery("case-alias", "docs are live", "0x" + __import__("hashlib").sha256(b"docs are live").hexdigest())
    direct_vm.mock_web(r"https://example\.com/delivery", {"status": 200, "body": "The required documentation is public."})
    direct_vm.mock_llm(r".*escrow delivery.*", json.dumps({"decision": "APPROVED", "criteria": [{"id": "docs", "result": "MET", "citations": ["https://example.com/delivery"], "reason": "Published."}], "summary": "Complete."}))
    assert contract.finalize_case("case-alias")["result"]["verdict"] == "FULFILLED"


def test_appeal_uses_authorized_stored_reason_and_is_bounded(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_alice)
    direct_vm.sender = direct_alice
    fund(direct_vm)
    contract.open_case("case-appeal", direct_bob, CRITERIA, URLS, "Publish docs")
    direct_vm.value = 0
    direct_vm.sender = direct_bob
    contract.submit_delivery("case-appeal", "docs are live", "0x" + __import__("hashlib").sha256(b"docs are live").hexdigest())
    direct_vm.mock_web(r"https://example\.com/delivery", {"status": 200, "body": "The required documentation is public."})
    direct_vm.mock_llm(r".*escrow delivery.*", json.dumps({"verdict": "FULFILLED", "settlement_bps": 10000, "findings": [{"criterion_id": "docs", "decision": "PASS", "citations": ["https://example.com/delivery"], "reason": "Published."}], "summary": "Complete."}))
    contract.finalize_case("case-appeal")

    direct_vm.sender = direct_alice
    appealed = contract.appeal_case("case-appeal", "The evidence was not available at review time.")
    assert appealed["appeal_count"] == 1
    assert appealed["appealed_by"] == appealed["sponsor"]
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"https://example\.com/delivery", {"status": 200, "body": "The required documentation is public."})
    direct_vm.mock_llm(r".*Authorized appeal reason from.*not available at review time.*", json.dumps({"verdict": "BREACHED", "settlement_bps": 0, "findings": [{"criterion_id": "docs", "decision": "FAIL", "citations": ["https://example.com/delivery"], "reason": "Not available."}], "summary": "Appeal upheld."}))
    result = contract.finalize_case("case-appeal")
    assert result["result"]["verdict"] == "BREACHED"

    with direct_vm.expect_revert("Appeal limit reached"):
        contract.appeal_case("case-appeal", "A second appeal should be rejected.")
