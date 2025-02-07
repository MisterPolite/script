import time
import sys
from urllib.parse import urlparse
from seleniumbase import Driver

if len(sys.argv) < 3:
    print("Usage: python rv3.py URL sitekey [cookie] [useragent]")
    sys.exit(1)

url = sys.argv[1]  
sitekey = sys.argv[2]  
cookie_string = sys.argv[3] if len(sys.argv) > 3 else ""
agent = sys.argv[4] if len(sys.argv) > 4 else ""
cookies = cookie_string.split("; ") if cookie_string else []
driver = Driver(browser="chrome", agent=agent, headless=True)
host = urlparse(url).hostname
for cookie in cookies:
    if "=" in cookie:
        name, value = cookie.split("=", 1)
        cookie_dict = {"name": name, "value": value, "domain": host}
        driver.execute_cdp_cmd("Network.setCookie", cookie_dict)

driver.get(url)
time.sleep(5)
try:
    token = driver.execute_script(f'return grecaptcha.execute("{sitekey}", {{action: "homepage"}});')
    driver.execute_script(f'document.querySelector("#recaptchav3Token").value = "{token}";')
    print("reCAPTCHA Token:", token)
except Exception as e:
    print("Error executing reCAPTCHA:", str(e))
try:
    token_value = driver.get_attribute("#token", "value")
    print("Extracted Token from Page:", token_value)
except Exception as e:
    print("Error extracting token from page:", str(e))
driver.quit()
