import requests
from .config import settings

def generate_data_contract(prompt: str):
    response = requests.post(
        settings.LLM_API_URL,
        json={"prompt": prompt},
        headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to generate data contract: " + response.text)
