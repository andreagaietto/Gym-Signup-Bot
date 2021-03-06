from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from configparser import SafeConfigParser
from datetime import datetime as dt
from datetime import timedelta
import datetime
#used for debugging
import time

link = None
target_date = dt.now().date() + timedelta(days=2)
target_formatted = target_date.strftime("%m/%d/%Y")
hour = dt.now().hour
minutes = dt.now().minute
if minutes <= 29:
    minutes = 00
else:
    minutes = 30
target_time = datetime.time(hour, minutes)
time_formatted = target_time.strftime("%#I:%M%p")

# create instance of webdriver and navigate to the correct page
driver = Chrome()
driver.get("https://www.ymcatriangle.org/northwest-cary-ymca-fitness-pool-gym-schedule")

# locate and select desired category
select = Select(driver.find_element_by_id('categoriesGXP'))
select.select_by_visible_text('Pool Schedule')
# get list of pool items for only the date I'm interested in. Can take awhile to load, so wait until elements exist to grab them
wait = WebDriverWait(driver, 10)
item_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-date=' + "'" +  target_formatted + "'" + ']')))
for item in item_list:
    # grab the parent
    parent_element = item.find_element_by_xpath("./..")
    # grab grandparent
    grandparent_element = parent_element.find_element_by_xpath("./..")
    # get the child of this element that lists the time slot
    time_slot = grandparent_element.find_element_by_class_name("GXPTime")
    # check to see if the time slot is the one we want, if it is, grab href and break out of loop
    slot_split = time_slot.text.split("-")
    if slot_split[0] == time_formatted:
        link_elem = item.find_element_by_xpath("./following-sibling::a[1]")
        link = link_elem.get_attribute('href')
        break
# go to proper signup page
driver.get(link)
# get my username and password, input into correct fields and submit
parser = SafeConfigParser()
parser.read('config.ini')
email = parser.get('signup_bot', 'email')
password = parser.get('signup_bot', 'password')
driver.find_element_by_id("login").send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_name('submit').click()
# click submit to finalize reservation
driver.find_element_by_name('submit').click()

driver.close()
driver.quit()







