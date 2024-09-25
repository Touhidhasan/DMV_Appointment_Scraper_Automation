from captcha_solver import CaptchaSolver
from sheet_reader import GoogleSheetReader
from email_sender import EmailSender
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time


class NYRTSSchedulerScraper:
    def __init__(self, driver):
        self.driver = driver
        self.saved_slots = []
        self.new_slots = []

    # Scrape available slot information from the page
    def scrape_info(self, location):
        with open('slots.txt', 'r') as file:
            self.saved_slots = [line.strip() for line in file]

        slot_dates = self.driver.find_elements(By.XPATH, '(//div[@class="owl-wrapper"])[1]//button')
        for slot_date in slot_dates:
            dates = slot_date.find_element(By.XPATH, './div').text.strip()
            if dates:
                self.new_slots.append(f"{location} {dates}")

        # Send emails for new slots and store them
        with open('slots.txt', 'a') as file:
            for slot in self.new_slots:
                if slot not in self.saved_slots:
                    print(f"Sending email for {slot}")
                    email_sender.send_email(slot)
                    file.write(slot + '\n')

    # Login to the DMV scheduler website
    def login(self, dmv_id_inp, month_inp, day_inp, year_inp, captcha_token):
        self.driver.get("https://nyrtsscheduler.com/")
        time.sleep(10)

        # Enter form details
        self.driver.find_element(By.XPATH, '//input[@id="ClientId"]').send_keys(dmv_id_inp)
        time.sleep(1)

        Select(self.driver.find_element(By.XPATH, '//select[@id="monthDropdown"]')).select_by_visible_text(month_inp)
        time.sleep(1)
        Select(self.driver.find_element(By.XPATH, '//select[@id="dayDropdown"]')).select_by_visible_text(day_inp)
        time.sleep(1)
        Select(self.driver.find_element(By.XPATH, '//select[@id="yearDropDown"]')).select_by_visible_text(year_inp)
        time.sleep(1)

        # Fill in CAPTCHA token and submit the form
        hidden_input = self.driver.find_element(By.XPATH, '//textarea[@id="g-recaptcha-response"]')
        self.driver.execute_script("arguments[0].value = arguments[1];", hidden_input, captcha_token)

        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        print('Login button clicked')

        time.sleep(5)

    # Main loop to scrape appointments based on locations
    def scrape_appointments(self, google_sheet_reader):
        while True:
            df = google_sheet_reader.get_data_from_first_sheet()
            for column in df.columns:
                location_list_inp = df[column].tolist()
                location_all = location_list_inp[0].lower() == "all"

                # Interact with form to input location details
                zip_input = self.driver.find_element(By.XPATH, '//input[@id="Zip"]')
                zip_input.clear()
                zip_input.send_keys(column)
                self.driver.find_element(By.XPATH, '//input[@id="btnContinueSelectTest"]').click()

                time.sleep(2)
                location = self.driver.find_element(By.XPATH, '(//h3[@class="col-md-12 h3-title text-left"])[1]').text
                location = location.replace("Select available dates at ", "").strip()

                if location_all or location.strip().lower() in [item.strip().lower() for item in location_list_inp]:
                    print(f"Location matched: {location}")
                    self.scrape_info(location)
                else:
                    print(f"Location not matched: {location}")
                self.driver.back()


if __name__ == "__main__":
    # Initialize services
    google_sheet_reader = GoogleSheetReader('key.json', 'nyrtsscheduler_scraper')
    email_sender = EmailSender("", "", "smtp.gmail.com", 587)
    captcha_solver = CaptchaSolver("", "https://nyrtsscheduler.com/", "6LdVtKscAAAAADEmOGVX_RR3htz0QYJrfTBrYExe")

    # Setup Chrome WebDriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    scraper = NYRTSSchedulerScraper(driver)

    # Solve CAPTCHA and login
    captcha_token = captcha_solver.solve_captcha()
    scraper.login("729003054", "April", "11", "2006", captcha_token)

    # Start scraping
    scraper.scrape_appointments(google_sheet_reader)
