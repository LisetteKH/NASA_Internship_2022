from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set the path to the Chrome WebDriver executable
webdriver_path = '/Users/norman/Library/chromedriverfolder/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# Specify the Chrome WebDriver path in the options
chrome_options.add_argument(f"webdriver.chrome.driver={webdriver_path}")

# Set up the Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the URL
URL = "https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_06/summary?keywords=rainfall"
driver.get(URL)

# Wait until the element with ID "docsContent" is present
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "docsContent")))

# Get the page source (HTML content)
page_source = driver.page_source

# Close the browser
driver.quit()

# Create a BeautifulSoup object with the page source
soup = BeautifulSoup(page_source, "html.parser")

# Find the div with ID "docsContent"
div_docs_content = soup.find('div', id='docsContent')

# Find all the <a> tags within the div
a_tags = div_docs_content.find_all('a')

# Define the file name and path
file_path = "/Users/norman/Documents/NASA/projects/NASA-GD-SU-Internship/pdfs.txt"

# Open the file in write mode
with open(file_path, 'w') as file:
    # Write the links to PDFs to the file
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href.endswith('.pdf'):
            file.write(href + '\n')

# Confirm the file was created
print(f"File created at '{file_path}'.")
