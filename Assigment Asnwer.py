import json
import base64

from indy import ledger, did

def give_consent(user_id: str, data_type: str, recipient_id: str) -> None:
    # Build the consent record
    consent_record = {
        "user_id": user_id,
        "data_type": data_type,
        "recipient_id": recipient_id,
        "timestamp": str(time.time())
    }

    # Encode the consent record as a JSON string
    consent_record_str = json.dumps(consent_record)

    # Submit the consent record to the blockchain
    response = ledger.submit_request(
        pool_handle=pool_handle,
        request_json=json.dumps({
            "operation": {
                "type": "100",
                "data": base64.b64encode(consent_record_str.encode("utf-8")).decode("utf-8")
            },
            "identifier": user_id,
            "signature": ""
        })
    )

    # Verify the response from the blockchain
    if response['op'] == 'REPLY':
        return True
    return False

def revoke_consent(user_id: str, data_type: str, recipient_id: str) -> None:
    # Build the consent record
    consent_record = {
        "user_id": user_id,
        "data_type": data_type,
        "recipient_id": recipient_id,
        "timestamp": str(time.time())
    }

    # Encode the consent record as a JSON string
    consent_record_str = json.dumps(consent_record)

    # Submit the consent revocation to the blockchain
    response = ledger.submit_request(
        pool_handle=pool_handle,
        request_json=json.dumps({
            "operation": {
                "type": "101",
                "data": base64.b64encode(consent_record_str.encode("utf-8")).decode("utf-8")
            },
            "identifier": user_id,
            "signature": ""
        })
    )

    # Verify the response from the blockchain
    if response['op'] == 'REPLY':
        return True
    return False

def check_consent(user_id: str, data_type: str, recipient_id: str) -> bool:
    # Build the consent record
    consent_record = {
        "user_id": user_id,
        "data_type": data_type,
        "recipient_id": recipient_id
    }

    # Encode the consent record as a JSON string
    consent_record_str = json.dumps(consent_record)

    # Query the blockchain for the consent record
    response = ledger.submit_request(
        pool_handle=pool_handle,
        request_json=json.dumps({
            "operation": {
                "type": "102",
                "data": base64.b64encode(consent_record_str.encode