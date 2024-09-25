import requests
import time

class CaptchaSolver:
    def __init__(self, api_key, site_url, site_key):
        self.api_key = api_key
        self.site_url = site_url
        self.site_key = site_key

    # Solve reCAPTCHA
    def solve_captcha(self):
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": 'ReCaptchaV2EnterpriseTaskProxyLess',
                "websiteKey": self.site_key,
                "websiteURL": self.site_url,
                "pageAction": "login",
            }
        }
        res = requests.post("https://api.capsolver.com/createTask", json=payload)
        task_id = res.json().get("taskId")
        if not task_id:
            print("Failed to create task:", res.text)
            return None

        while True:
            time.sleep(1)
            result_res = requests.post("https://api.capsolver.com/getTaskResult", json={"clientKey": self.api_key, "taskId": task_id})
            if result_res.json().get("status") == "ready":
                return result_res.json().get("solution", {}).get('gRecaptchaResponse')
            if result_res.json().get("status") == "failed":
                print("CAPTCHA solve failed!")
                return None
