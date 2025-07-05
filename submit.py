import requests
import pyotp
import base64
from base64 import b64encode

email = "reddygurupraneethreddy@gmail.com"  
gist_url = "https://gist.github.com/gurupraneethreddy/4e3adb021e34a751e04cdb7c78b67e17"
solution_language = "python"

shared_secret = email + "HENNGECHALLENGE004"
shared_secret_bytes = shared_secret.encode('utf-8')
base32_secret = base64.b32encode(shared_secret_bytes).decode('utf-8')

totp = pyotp.TOTP(
    base32_secret,
    digits=10,
    digest="sha512",
    interval=30
)
totp_code = totp.now()
print(f"TOTP Code: {totp_code}") 

json_data = {
    "github_url": gist_url,
    "contact_email": email,
    "solution_language": solution_language
}

auth = b64encode(f"{email}:{totp_code}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth}"
}

url = "https://api.challenge.hennge.com/challenges/backend-recursion/004"
try:
    response = requests.post(url, json=json_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.RequestException as e:
    print(f"Error: {e}")