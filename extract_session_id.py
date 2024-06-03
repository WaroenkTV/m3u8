import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define the URL
url = 'https://www.cubmu.com/play/live-tv?id=4028c68574537fcd0174be58644c5901&genreId=10'
# Use GITHUB_WORKSPACE environment variable to define the output file path
output_file = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), 'tvs_token.txt')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode for faster execution
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver using WebDriver Manager
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time if necessary

# Extract cookies
cookies = driver.get_cookies()
tvs_token = None

# Find the tvs_token in cookies
for cookie in cookies:
    if cookie['name'] == 'tvs_token':
        tvs_token = cookie['value']
        break

# Check if tvs_token is found and save only the value to a file
if tvs_token:
    with open(output_file, 'w') as file:
        file.write(tvs_token)
    print(f'tvs_token found and saved to {output_file}')
else:
    print('tvs_token not found')

# Close the browser
driver.quit()
