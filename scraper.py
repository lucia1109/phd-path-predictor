from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time



CHROMEDRIVER_PATH = r"C:\Users\user\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--headless")  # Run without opening the browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Usually helps on Windows
options.add_argument("--window-size=1920,1080")  # Set a window size

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Rest of your scraping code follows...


url = "https://www.eecs.mit.edu/academics/graduate-programs/graduate-research/"
driver.get(url)

# Give the page time to fully load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "strong"))
)

strongs = driver.find_elements(By.TAG_NAME, "strong")
print(f"Found {len(strongs)} <strong> elements")

programs = []

for s in strongs:
    program_name = s.text.strip()
    print("-", program_name)
    if program_name:
        programs.append({
            "university": "MIT",
            "program": f"PhD in {program_name}",
            "location": "Cambridge, MA",
            "funding": "Yes",
            "visa_support": "Yes",
            "gre_required": "No"
        })

driver.quit()

with open("data/programs.json", "w") as f:
    json.dump(programs, f, indent=2)

print(f"Saved {len(programs)} programs to data/programs.json")
