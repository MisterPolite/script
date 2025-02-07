# pip install seleniumbase
# python turnstile.py https://example.com/turnstile
# only work turnstile autoload
from seleniumbase import SB
import time
import json
import sys
def open_the_turnstile_page(sb, url):
    sb.driver.uc_open_with_reconnect(url, reconnect_time=5)

def click_turnstile_and_verify(sb):
    try:
        sb.driver.uc_click("span[role='checkbox']")
    except Exception:
        pass
    sb.switch_to_default_content()
    token = sb.driver.execute_script("""return document.querySelector('input[name="cf-turnstile-response"]')?.value""")
    return token
if len(sys.argv) < 2:
    print(json.dumps({"status": False, "message": "no url provided"})) 
    sys.exit(1)
url = sys.argv[1]

with SB(uc=True, test=False, headless=True) as sb:
    open_the_turnstile_page(sb, url)
    time.sleep(5)
    try:
        token = click_turnstile_and_verify(sb)
        status = "true" if token else "false"
        response = {"status": status, "token": token if token else None}
        print(json.dumps(response))
    except Exception as e:
        open_the_turnstile_page(sb)
        token = click_turnstile_and_verify(sb)
        status = "true" if token else "false"
        response = {"status": status, "token": token if token else None}
        print(json.dumps(response)) 
