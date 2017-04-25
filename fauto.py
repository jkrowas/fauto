import splinter as sp
import time

username = 'username'
password = 'password'
landing_url = 'https://chanzuckerberg.preprod.fluxxlabs.com/user_sessions/new'

with sp.Browser('chrome') as browser:

    browser.visit(landing_url)
    browser.find_by_id('user_session_login').fill(username)
    browser.find_by_id('user_session_password').fill(password)
    button = browser.find_by_value('Sign in')
    button.click()

    if (browser.is_text_present('Invalid Credentials')):
        print("Can't log in; invalid credentials")
    else:
        print ('Successful login')

