import requests

def trigger_bland_call():
    """Initiate a call via Bland API"""
    payload = {
        "phone_number": "+91 9442637368",  # Replace with dynamic patient/guardian number
        "pathway_id": "dddf5030-d3cd-428d-a453-b27be9b48ea9"
    }
    headers = {
        "authorization": "org_2789db9c7b978960a155d6c32c6fd1198c22b7a7b7586f7d78bb00a9150b50364033f445a6ba5710b50d69",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.bland.ai/v1/calls", json=payload, headers=headers)
    if response.status_code == 200:
        return True, "📞 Emergency call initiated successfully!"
    else:
        return False, f"⚠️ Call failed: {response.text}"
