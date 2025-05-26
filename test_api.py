import requests
import base64
import time

base_url = "http://localhost:8000"
email = "user@example.com"
password = "string"
image_path = "Crazy_Frog_Standing.png"

login_data = {"email": email, "password": password}
response = requests.post(f"{base_url}/login/", json=login_data)
token = response.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

with open(image_path, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()

image_data = {"image": image_base64, "algorithm": "sauvola"}
response = requests.post(f"{base_url}/binary_image", json=image_data, headers=headers)
task_id = response.json().get("task_id")
print(f"Task ID: {task_id}")

while True:
    response = requests.get(f"{base_url}/task/{task_id}", headers=headers)
    status_data = response.json()
    print(status_data)
    if status_data["status"] in ["COMPLETED", "FAILURE"]:
        break
    time.sleep(2)