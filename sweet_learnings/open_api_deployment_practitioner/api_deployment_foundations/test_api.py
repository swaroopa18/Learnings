
import json

# Mock API specification
BASE_URL = "<MOCK_BASE_URL>"
ENDPOINT = "/classify-ticket"

def mock_api(payload):
    """Simulate the API locally; no network requests."""
    if "ticket_text" not in payload:
        return 400, {"detail": "ticket_text is required"}

    text = payload["ticket_text"]

    if not isinstance(text, str) or not text.strip():
        return 400, {"detail": "ticket_text is required"}

    return 200, {
        "category": "damaged_item",
        "summary": (
            "Customer reports a damaged package and needs "
            "help with a replacement."
        )
    }


# TEST 1: Valid request
status, body = mock_api({
    "ticket_text": (
        "My package arrived damaged and I need help "
        "with a replacement."
    )
})

print("Test 1 - Valid ticket")
print("Status:", status)
print("Response:", json.dumps(body, indent=2))
assert status == 200
assert body["category"] == "damaged_item"
print("PASS\n")


# TEST 2: Empty JSON body
status, body = mock_api({})

print("Test 2 - Empty body")
print("Status:", status)
print("Response:", json.dumps(body, indent=2))
assert status == 400
assert body["detail"] == "ticket_text is required"
print("PASS\n")


# TEST 3: Empty string
status, body = mock_api({"ticket_text": ""})

print("Test 3 - Empty ticket text")
print("Status:", status)
print("Response:", json.dumps(body, indent=2))
assert status == 400
print("PASS\n")

print("All 3 offline tests passed.")
