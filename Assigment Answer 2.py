import json
from indy import anoncreds, wallet
from indy.error import IndyError

async def give_consent(user_id: str, data_type: str, recipient_id: str):
    try:
        # Open wallet
        wallet_handle = await wallet.open_wallet("wallet", None, None)

        # Create a master secret
        await anoncreds.prover_create_master_secret(wallet_handle, None)

        # Create a claim offer
        offer_json = json.dumps({
            "issuer_did": user_id,
            "schema_seq_no": data_type,
            "claim_def_seq_no": recipient_id
        })

        # Store the claim offer in the wallet
        await anoncreds.prover_store_claim_offer(wallet_handle, offer_json)

        print("Consent has been given by user: {} for data type: {} to be shared with recipient: {}".format(user_id, data_type, recipient_id))

    except IndyError as e:
        print("Error giving consent: ", e)

async def revoke_consent(user_id: str, data_type: str, recipient_id: str):
    try:
        # Open wallet
        wallet_handle = await wallet.open_wallet("wallet", None, None)

        # Search for claim offer
        search_handle = await anoncreds.prover_search_claims(wallet_handle, "{}")

        claims = json.loads(await anoncreds.prover_fetch_claims(search_handle))
        for claim in claims:
            if claim["issuer_did"] == user_id and claim["schema_seq_no"] == data_type and claim["claim_def_seq_no"] == recipient_id:
                # Remove the claim offer from the wallet
                await anoncreds.prover_delete_claim(wallet_handle, claim["referent"])
                print("Consent has been revoked by user: {} for data type: {} to be shared with recipient: {}".format(user_id, data_type, recipient_id))
                break
        else:
            print("Consent does not exist for the given user, data type and recipient.")

    except IndyError as e:
        print("Error revoking consent: ", e)

async def check_consent(user_id: str, data_type: str, recipient_id: str) -> bool:
    try:
        # Open wallet
        wallet_handle = await wallet.open_wallet("wallet", None, None)

        # Search for claim offer
        search_handle = await anoncreds.prover_search_claims(wallet_handle, "{}")

        claims = json.loads(await anoncreds.prover_fetch_claims(search_handle))
        for claim in claims:
            if claim["issuer_did"] == user_id and claim["schema_seq_no"] == data_type and claim["claim_def_seq_no"] == recipient_id:
                return True

        return False

