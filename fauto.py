import splinter as sp
import time
from pywinauto import Application
import logging


#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

test_landing_url = "https://chanzuckerberg.preprod.fluxxlabs.com/user_sessions/new"
prod_landing_url = "https://chanzuckerberg.fluxx.io/user_sessions/new"
username = 'nina@chanzuckerberg.com'
password = 'Welcome!'
grant_id = 'HCA-A-1703-00264'
upload_file = '00264.pdf'

url = test_landing_url
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
            logger.info("Login Worked!")

    except:
        logger.fatal("Can't login on page %s" , url)

    browser.is_text_present('Applications', wait_time=5)
    apps_card = browser.find_by_text('Applications').first
    # # Look for an open application
    # i = browser.find_by_tag("i")
    # for j in i:
    #     if j.has_class("futil u-arrowl-f"):
    #         j.click()
    logger.info("Finding Application %s", grant_id)
    myapp = apps_card.find_by_text(grant_id)
    if len(myapp) > 0:
        logger.info("Found Application %s!", grant_id)
    myapp.click()
    #wf = apps_card.find_by_text('Workflow')
    #wf.click()
    #note = browser.find_by_tag('textarea').first
    #time.sleep(5)
    #if note.has_class('optional-workflow-note'):
    #    note.fill("Foo")
    time.sleep(2)
    if browser.is_element_present_by_text("\nInternal Documents\n", wait_time = 5):
        id = browser.find_by_text("\nInternal Documents\n")
        i = id.find_by_tag('i')
        print (len(i))
        for j in i:
            if j.has_class('futil u-cplus-f'):
                print (j.value)
                j.click()
                if browser.is_element_present_by_text('Add files', wait_time = 5):
                    browser.find_by_text('Add files').click()
                    time.sleep(1)
                    app = Application().connect(title="Open")
                    logger.info("Uploading document %s", upload_file)
                    app.Open.Edit.set_edit_text(upload_file)
                    app.Open.Cancel.close_click()
                    browser.find_by_text('Close').click()
                else:
                    logger.info("Can't find Add Files button")
    else:
        logger.info("Couldn't find Internal Documents Section")




