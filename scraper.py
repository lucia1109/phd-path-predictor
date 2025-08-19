from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

CHROMEDRIVER_PATH = r"C:\Users\user\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Headless options
options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# -------------------------------
# Multiple sites to scrape
# -------------------------------
sites = [
    {
        "university": "MIT",
        "url": "https://www.eecs.mit.edu/academics/graduate-programs/graduate-research/",
        "location": "Cambridge, MA",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "Yes",
        "tag": "strong"
    },
    {
        "university": "Stanford",
        "url": "https://cs.stanford.edu/admissions/phd",
        "location": "Stanford, CA",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "Yes",
        "tag": "h2"
    },
    {
        "university": "University of Waterloo",
        "url": "https://uwaterloo.ca/current-graduate-students/catalogs/graduate-funding-and-awards-database/sp-pasupalak-scholarship-robotics",
        "location": "Waterloo, Canada",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "No",
        "tag": "h1"
    },
    {
        "university": "University of British Columbia",
        "url": "https://unisa.edu.au/research/degrees/scholarships/the-william-t-southcott-scholarship/",
        "location": "Vancouver, Canada",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "No",
        "tag": "title"
    },
    {
        "university": "University of South Australia",
        "url": "https://careanywhere.ubc.ca/grad-training-program/how-to-apply/",
        "location": "Australia",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "No",
        "tag": "title"
    },
    {
        "university": "University of New England",
        "url": "https://www.une.edu.au/research/graduate-research-school/scholarships/machine-learning-modelling-to-analyse-medical-and-educational-data-including-imaging-video-and-test-based-reports",
        "location": "Australia",
        "gre_required": "No",
        "funding": "Yes",
        "visa_support": "No",
        "tag": "title"
    },
]

programs = []

# Loop over each site
for site in sites:
    print(f"Scraping: {site['university']}")
    driver.get(site["url"])

    try:
        # Wait up to 10 seconds for elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, site["tag"]))
        )

        #soup.find_all("TAG", {"class": "CLASSNAME"})

        elements = driver.find_elements(By.TAG_NAME, site["tag"])
        print(f"Found {len(elements)} <{site['tag']}> elements")

        for el in elements:
            program_name = el.text.strip()
            if program_name:
                print("-", program_name)
                programs.append({
                    "university": site["university"],
                    "program": f"PhD in {program_name}",
                    "location": site["location"],
                    "funding": site["funding"],
                    "visa_support": site["visa_support"],
                    "gre_required": site["gre_required"]
                })

    except Exception as e:
        print(f"Error scraping {site['university']}: {e}")

driver.quit()

with open("data/programs.json", "w") as f:
    json.dump(programs, f, indent=2)

print(f"✅ Saved {len(programs)} total programs to data/programs.json")
