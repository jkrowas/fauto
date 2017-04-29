import splinter as sp
import time
from pywinauto import Application
import logging
import sys
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

test_landing_url = "https://chanzuckerberg.preprod.fluxxlabs.com/user_sessions/new"
prod_landing_url = "https://chanzuckerberg.fluxx.io/user_sessions/new"
username = 'nina@chanzuckerberg.com'
password = 'Welcome!'
grant_id = 'HCA-A-1703-00264'
upload_file = "c:\\temp\\OISP_July.pdf"

url = test_landing_url


def get_grants_to_process(filename):
    grants = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            grants.append(row[0])
    return grants


def do_upload(browser, apps_card, grant_id, upload_file):
    logger.debug("Beginning upload of %s for grant %s",  upload_file, grant_id)
    time.sleep(2)
    logger.info("Finding Application %s", grant_id)
    myapp = apps_card.find_by_text(grant_id)
    if len(myapp) > 0:
        logger.info("Found Application %s", grant_id)
    else:
        logger.info("Couldn't find Application %s!", grant_id)
        return(1)
    myapp.click()
    time.sleep(2)
    try:
        if browser.is_element_present_by_text("\nInternal Documents\n", wait_time=5):
            id = browser.find_by_text("\nInternal Documents\n")
            time.sleep(2)
            i = id.find_by_tag('i')
            for j in i:
                if j.has_class('futil u-cplus-f'):  # Add Document button
                    print(j.value)
                    j.click()
                    if browser.is_element_present_by_text('Add files', wait_time=5):
                        browser.find_by_text('Add files').click()
                        time.sleep(1)
                        app = Application().connect(title="Open")
                        logger.info("Uploading document %s", upload_file)
                        app.Open.Edit.set_edit_text(upload_file)
                        app.Open.Open.close_click()
                        browser.select("plupload_file_type", "3417")  # 3417 is "Other Document"
                        browser.find_by_text('Start upload').click()
                        browser.is_text_present('Upload Complete!', wait_time=60)
                        logger.info("Upload complete")
                        browser.find_by_text('Close').click()
                        return 0
                    else:
                        logger.info("Can't find Add Files button")
                        return 1
        else:
            logger.warning("Couldn't find Internal Documents Section")
            return 1
    except:
        logger.error("Unexpected error: %s while processing grant %s", str(sys.exc_info()[0]), grant_id)
        return 0


with sp.Browser('chrome') as browser:
    # Visit URL
    browser.visit(url)
    try:
        logger.info("Attempting to log in to %s", url)
        browser.find_by_id('user_session_login').fill(username)
        browser.find_by_id('user_session_password').fill(password)
        button = browser.find_by_name('commit')
        button.click()
        if browser.is_text_present('Invalid Credentials'):
            logger.fatal("Login failed; invalid credentials")
        else:
            logger.info("Login successful!")

    except:
        logger.fatal("Can't login on page %s" , url)

    browser.is_text_present('Applications', wait_time=5)
    apps_card = None
    apps = browser.find_by_text('Applications')
    for a in apps:
        if a.has_class('card_name title'):
            apps_card = a
    if apps_card is not None:
        logger.info("Found Applications card")
    else:
        logger.info("Couldn't find Applications card, exiting")
        exit()

    grants = get_grants_to_process("c:\\users\\kr9\\PycharmProjects\\fauto\\grants.csv")
    logger.info("Doing %i grants", len(grants))
    success_count = 0
    unprocessed = []
    for g in grants:
        upload_file = "c:\\temp\\" + g + ".pdf"
        if do_upload(browser, apps_card, g, upload_file) != 0:
            unprocessed.append(str(g))
            logger.warning("Couldn't complete upload for %s", g)
        else:
            success_count += 1

    logger.info("Processed %i/%i grants successfully", success_count, len(grants))
    if len(unprocessed) > 0:
        logger.warning("These applications were not processed: %s", ', '.join(unprocessed))







