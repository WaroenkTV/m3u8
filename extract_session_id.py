from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import base64
import json
import time

# Set up Chrome options
options = Options()
options.headless = True  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver
driver_service = Service(executable_path="/usr/local/bin/chromedriver")  # Ensure this path is correct
driver = webdriver.Chrome(service=driver_service, options=options)

try:
    # Navigate to the URL
    url = "https://www.cubmu.com/play/live-tv?id=4028c68574537fcd0174be58644c5901&genreId=10"
    driver.get(url)

    # Allow some time for the page to load and the token to be set
    time.sleep(10)  # Adjust the sleep time if needed

    # Extract the session token from cookies
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'tvs_token':
            tvs_token = cookie['value']
            break

    # Decode the JWT token to get the sessionId
    base64_url = tvs_token.split('.')[1]
    base64_str = base64_url.replace('-', '+').replace('_', '/')
    json_payload = base64.b64decode(base64_str).decode('utf-8')

    payload = json.loads(json_payload)
    session_id = payload['currentSessionId']

    # Write the sessionId to a text file
    with open('session_id.txt', 'w') as file:
        file.write(session_id)

finally:
    # Close the driver
    driver.quit()
