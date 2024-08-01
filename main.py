# created by 0xkuzey 
# discord.gg/clown

import requests
import tls_client
import time
import random
import threading

api_key = "ur cap solver key"  # capsolver.com
site_key = "9c54b617-bd43-4858-a8c9-83ce00be8180" 
site_url = "https://paste.fo/" 

def get_random_proxy():
    with open('proxy.txt', 'r') as file:
        proxies = file.readlines()
    proxy = random.choice(proxies).strip()
    return proxy

def get_random_title():
    with open('title.txt', 'r') as file:
        titles = file.readlines()
    title = random.choice(titles).strip()
    return title

def get_random_content():
    with open('content.txt', 'r') as file:
        contents = file.readlines()
    content = random.choice(contents).strip()
    return content

# CAPTCHA token'ını al
def get_captcha_token():
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'HCaptchaTaskProxyLess',
            "websiteKey": site_key,
            "websiteURL": site_url
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("Failed to create task:", res.text)
        return None
    print(f"Got taskId: {task_id} / Getting result...")

    while True:
        time.sleep(1)
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            return resp.get("solution", {}).get('gRecaptchaResponse')
        if status == "failed" or resp.get("errorId"):
            print("Solve failed! Response:", res.text)
            return None

def send_request():
    proxy = get_random_proxy()
    print(f"Using proxy: {proxy}")

    proxies = {
        "http": proxy,
        "https": proxy
    }

    token = get_captcha_token()
    if not token:
        print("Failed to get captcha token")
        return

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://paste.fo',
        'priority': 'u=0, i',
        'referer': 'https://paste.fo/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    title = get_random_title() 
    content = get_random_content() 
    data = {
        'title': title, 
        'syntax': 'plain',
        'expire': '0',
        'visibility': 'public',
        'password': '',
        'hcap': token,
        'g-recaptcha-response': token,
        'h-captcha-response': token,
        'content': content, 
    }

    with tls_client.Session(
        client_identifier="chrome_126",
        random_tls_extension_order=True
    ) as session:
        response = session.post('https://paste.fo/create', headers=headers, data=data)
        print(response.text)

def main():
    num_requests = int(input("How many requests do you want to send? "))
    threads = []

    for _ in range(num_requests):
        t = threading.Thread(target=send_request)
        t.start()
        threads.append(t)
        time.sleep(0.1) 

    for t in threads:
        t.join()  

if __name__ == "__main__":
    main()