from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import time


# read botnetConfig.json data
with open('botnetConfig.json') as data_file:
    botnet = json.load(data_file)
print(botnet)
bots = botnet["bots"]

for bot in bots:
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(executable_path='/home/nau/sourceProgramsToInstall/geckodriver')


    # TEMP MAIL GENERATE
    print "Opening temp-mail.org to create an email account"
    driver.get("https://temp-mail.org/en/")
    email = driver.find_element_by_id("mail").get_attribute("value")
    print email

    # Save the window opener (current window, do not mistaken with tab... not the same)
    window_email = driver.window_handles[0]
    # open new tab
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + "t")

    #
    # TWITTER SIGNUP
    #
    print "Opening twitter.com/signup to create a twitter account"
    driver.execute_script('''window.open("http://www.twitter.com/signup","_blank");''')

    # Save the window opener (current window, do not mistaken with tab... not the same)
    window_twitter = driver.window_handles[1]
    # Put focus on current window which will, in fact, put focus on the current visible tab
    driver.switch_to_window(window_twitter)

    delay = 10 # seconds
    # wait until the page is loaded, in this case, wait unitl the element with id='full-name' is loaded
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'full-name')))

    print driver.title

    driver.find_element_by_id("full-name").send_keys(bot["full-name"])
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("password").send_keys(bot["password"])
    driver.find_element_by_id("submit_button").submit()


    # PHONE Verification
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'phone_number')))
    driver.find_element_by_id("phone_number").send_keys(botnet["phone-number"])
    driver.find_element_by_name("discoverable_by_mobile_phone").click()#checkbox click
    driver.find_element_by_name("call_me").submit()


    code = raw_input('input something!: ')
    driver.find_element_by_id("code").send_keys(code)
    driver.find_element_by_id("code").submit()


    #
    # TWITTER APPS TOKEN GENERATION
    #
    print "Opening https://apps.twitter.com/ to generate a twitter API tokens"
    driver.execute_script('''window.open("https://apps.twitter.com/","_blank");''')
    # Save the window opener (current window, do not mistaken with tab... not the same)
    window_twitterApps = driver.window_handles[2]
    # Put focus on current window which will, in fact, put focus on the current visible tab
    driver.switch_to_window(window_twitterApps)
    driver.find_elements_by_xpath("//*[contains(text(), 'Create New App')]")[0].click()

    driver.find_element_by_id("edit-name").send_keys(bot["full-name"] + "App")
    driver.find_element_by_id("edit-description").send_keys(bot["full-name"] + " is a good app")
    driver.find_element_by_id("edit-url").send_keys("http://twitter.com")
    driver.find_element_by_name("edit-tos-agreement").click()#checkbox click

    driver.find_element_by_id("edit-submit").submit()

    #generate tokens
    driver.find_elements_by_xpath("//*[contains(text(), 'Keys and Access Tokens')]")[0].click()
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'edit-submit-owner-token')))
    driver.find_element_by_id("edit-submit-owner-token").submit()

    # get the tokens
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'edit-token-actions')))

    consumerKey = driver.find_elements_by_xpath("//*[contains(text(), 'Consumer Key (API Key)')]/following-sibling::span")[0].text
    consumerSecret = driver.find_elements_by_xpath("//*[contains(text(), 'Consumer Secret (API Secret)')]/following-sibling::span")[0].text
    accessToken = driver.find_elements_by_xpath("//*[contains(text(), 'Access Token')]/following-sibling::span")[0].text
    accessTokenSecret = driver.find_elements_by_xpath("//*[contains(text(), 'Access Token Secret')]/following-sibling::span")[0].text

    botnetConfig["consumerKey"] = consumerKey
    botnetConfig["consumerSecret"] = consumerSecret
    botnetConfig["accessToken"] = accessToken
    botnetConfig["accessTokenSecret"] = accessTokenSecret

    with open('results.txt', 'w') as outfile:
        json.dump(botnetConfig, outfile)
