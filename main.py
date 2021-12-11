import logging
from atexit import register
from sys import stdout
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import telegram

# Define logger
logger = logging.getLogger('default_logger')

logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

driver = webdriver.Remote("http://selenium:4444")

primary_url = "https://telegov.njportal.com/njmvc/AppointmentWizard/15"

valid_location_names = [
    "Bayonne",
    "Elizabeth",
    "Lodi",
    "Newark",
    "North Bergen",
    "Wayne",
    "Paterson",
]

save = False


@register
def cleanup():
    driver.quit()


def main():
    logger.info("Getting page...")
    driver.get(primary_url)

    if save:
        logger.info("Saving page...")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    locations = driver.find_elements(
        by=By.XPATH,
        value='//div[@class="input-group input-group-sm"]//div[@class="text-capitalize"]',
    )
    appointments_found = False
    for location in locations:
        try:
            appointment_button = location.find_element(by=By.XPATH, value=".//a[@class='btn btn-secondary btn-xs mt-1']")
            location_name = location.find_element(by=By.TAG_NAME, value="span").text
            location_name = location_name.replace("Permits/License", "").strip()
            if location_name in valid_location_names:
                logger.info(f"Found {location_name}. Getting appointment page...")
                href = appointment_button.get_attribute("href")
                href = href.replace("javascript:NavigatetoDateTime(", "").replace(");", "")
                appointment_url = primary_url + "/" + href
                logger.info(f"Pushing {appointment_url} ...")
                appointments_found = True
        except NoSuchElementException:
            continue
    if not appointments_found:
        logger.info("No appointments found.")


if __name__ == '__main__':
    logger.info("Starting...")
    while True:
        main()
        logger.info("Sleeping for 1 minute...")
        sleep(60)
        logger.info("Done sleeping.")
