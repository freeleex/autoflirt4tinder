import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random
from random import randint
import urllib
import requests as r

from secrets import user, password, url
from pickups import pickups


# Initialization of the driver
driver = webdriver.Chrome('./chromedriver')
driver.get("https://www.tinder.com")

# Initialization of global variables
photo_index = 1
per_to_like = .7  # Percentage to like (In decimals)
min_punctuation = 7  # Minimum punctuation to give like

# Log the info
girls_no = 0
likes_no = 0
dislikes_no = 0
matches_no = 0


# Login
def log_in():
    global girls_no
    global likes_no
    global dislikes_no
    global matches_no

    # All the sleeps are to make sure that everything is loaded
    # so it doesn't throw an error
    sleep(1)

    # Accept the terms and click on login
    find_by_xpath_btn('//*[@id="content"]/div/div[2]/div/div/div[1]/button')
    find_by_xpath_btn('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button')

    sleep(2)

    # Select "Login with google"
    find_by_xpath_btn('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[1]/div/button')

    base_window = driver.window_handles[0]  # Save our actual window
    driver.switch_to.window(driver.window_handles[1])  # Change to the new window

    # Insert username and password
    find_by_xpath_input('//*[@id="identifierId"]', user)
    find_by_xpath_btn('//*[@id="identifierNext"]/div/button')

    sleep(2)

    find_by_xpath_input('//*[@id="password"]/div[1]/div/div[1]/input', password)
    find_by_xpath_btn('//*[@id="passwordNext"]/div/button')

    sleep(5)

    driver.switch_to.window(base_window)  # Return to our previous window

    find_by_xpath_btn('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    find_by_xpath_btn('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')

    sleep(3)

    while True:
        auto_swipe()  # Start swiping!


def auto_swipe():
    sleep(0.5)
    global photo_index

    # If you just want to give like to everyone uncomment this section
    # if True:
    #     like()
    #    return
    # ----------------------------------------------------------------

    try:
        # Check if it isn't the last photo
        attractive_div = driver.find_element_by_xpath(
            f'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span['
            f'{photo_index}]/div')
    except Exception:
        # Randomly give like or dislike
        rand = random()
        if rand < per_to_like:
            like()
        else:
            dislike()
        photo_index = 1
        return

    # Get the URL of the image from the HTML element
    attractive_style1 = attractive_div.get_attribute('style')
    attractive_style_2 = attractive_style1[attractive_style1.find('"') + 1:len(attractive_style1)]
    img_url = attractive_style_2[0:attractive_style_2.find('"')]

    urllib.request.urlretrieve(img_url, "girl.jpg")  # Download the image
    sleep(1)

    # Send the image to the AI to check its attractiveness
    response = r.post(url, data=open('girl.jpg', 'rb')).text
    json_response = json.loads(response)

    # If the response isn't empty get the attractiveness and decide to give like or dislike
    if json_response['people']:
        print(json_response['people'][0])
        attractiveness = json_response['people'][0]['attractiveness']
        if attractiveness > min_punctuation:
            like()
        else:
            dislike()
        photo_index = 1
    else:
        # If the response is empty, pass to the next photo
        print("Couldn't recognize any face")
        driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
        photo_index += 1


# Give like
def like():
    global girls_no
    global likes_no
    girls_no += 1
    likes_no += 1
    find_by_xpath_btn('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
    sleep(1)
    check_popups()  # Check if there's any popup before give like


# Give dislike
def dislike():
    global girls_no
    global dislikes_no
    girls_no += 1
    dislikes_no += 1
    find_by_xpath_btn('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
    sleep(1)
    check_popups()  # Check if there's any popup before give like


def match():
    match_input = driver.find_element_by_xpath('//*[@id="chat-text-area"]')
    send_btn = driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button')
    pickup = pickups[randint(0, len(pickups) - 1)]  # Select a random pickup line

    global matches_no
    matches_no += 1
    print_stats()
    match_input.send_keys(pickup)  # Send the pickup line
    sleep(0.5)
    send_btn.click()  # Continue
    sleep(1)


def print_stats():
    print('-----------------------------------')
    print('Number of girls found: ', girls_no)
    print('Number of likes: ', likes_no)
    print('Number of dislikes: ', dislikes_no)
    print('Number of matches: ', matches_no)
    print('-----------------------------------')


def check_popups():
    try:
        match()
    except Exception:
        try:
            find_by_xpath_btn('//*[@id="modal-manager"]/div/div/div[2]/button[2]')  # Close popup
        except Exception:
            try:
                find_by_xpath_btn('//*[@id="modal-manager"]/div/div/button[2]')  # Close super like popup
            except Exception:
                sleep(0)


# Find a button on the html by the xpath and click it
def find_by_xpath_btn(xpath):
    btn = driver.find_element_by_xpath(xpath)
    btn.click()


# Send an input in the html and fill it
def find_by_xpath_input(xpath, text):
    input_field = driver.find_element_by_xpath(xpath)
    input_field.send_keys(text)


if __name__ == '__main__':
    log_in()
