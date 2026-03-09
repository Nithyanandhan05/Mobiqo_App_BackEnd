import requests

def test_admin_dashboard():
    # Login to get token
    login_url = "http://127.0.0.1:5000/login"
    login_data = {
        "email": "admin@gmail.com",
        "password": "admin"
    }
    
    try:
        res = requests.post(login_url, json=login_data)
        data = res.json()
        print("Login Response:", data)
        
        if data.get('status') == 'success':
            token = data.get('token')
            
            # Fetch dashboard
            dash_url = "http://127.0.0.1:5000/admin/dashboard"
            headers = {"Authorization": f"Bearer {token}"}
            dash_res = requests.get(dash_url, headers=headers)
            print("\nDashboard Status:", dash_res.status_code)
            print("Dashboard Response:", dash_res.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_admin_dashboard()
