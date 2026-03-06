import requests

# We are hitting your local Flask server
url = "http://127.0.0.1:5000/admin/warranties/1/approve" # Assuming Warranty ID 1 exists

# We are sending the 'Approve' command
payload = {"action": "Approve"}

# Note: You will need a valid Admin JWT token here to pass security!
# (For a quick test, you can temporarily remove @jwt_required() from the approve_warranty route in admin.py)
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_ADMIN_TOKEN_HERE" 
}

print("Simulating Admin clicking 'Approve'...")
response = requests.put(url, json=payload, headers=headers)

print("Server Response:", response.text)