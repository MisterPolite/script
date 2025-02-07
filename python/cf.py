# pip install seleniumbase
# python cf.py https:example.com/cloudflare
import os
import sys
import time
import json
import warnings
from seleniumbase import Driver
# only work with cloudflare with auto load
url = sys.argv[1]
driver = Driver(uc=True, headless=True)

def Cloudflare():
    title = driver.title
    if any(sub.lower() in title.lower() for sub in ["cloudflare", "just a moment..."]):
        time.sleep(10)
        return False
    return True
try:
    driver.uc_open_with_reconnect(url, reconnect_time=5)
    while not Cloudflare():
        time.sleep(3)
    cf_clearance = driver.get_cookie("cf_clearance")
    cf_clearance = cf_clearance["value"] if cf_clearance else None
    user_agent = driver.execute_script("return navigator.userAgent;")
    data = {"cf_clearance": cf_clearance, "user-agent": user_agent}
except Exception as e:
    print(json.dumps({"error": str(e)}), file=sys.stderr)
    data = {"cf_clearance": False, "user-agent": None}
finally:
    print(json.dumps(data))
    try:
        driver.quit()
    except Exception:
        pass
