from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#used for debugging
import time

link = None

# create instance of webdriver and navigate to the correct page
driver = Chrome()
driver.get("https://www.ymcatriangle.org/northwest-cary-ymca-fitness-pool-gym-schedule")

# locate and select desired category
select = Select(driver.find_element_by_id('categoriesGXP'))
select.select_by_visible_text('Pool Schedule')
# get list of pool items for only the date I'm interested in - refactor for flexibility. Can take awhile to load, so wait until elements exist to grab them
wait = WebDriverWait(driver, 10)
item_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-date='11/07/2021']")))
for item in item_list:
    # grab the parent
    parent_element = item.find_element_by_xpath("./..")
    # grab grandparent
    grandparent_element = parent_element.find_element_by_xpath("./..")
    # get the child of this element that lists the time slot
    time_slot = grandparent_element.find_element_by_class_name("GXPTime")
    # check to see if the time slot is the one we want, if it is, grab href and break out of loop
    if time_slot.text == "1:00PM-1:30PM":
        link_elem = item.find_element_by_xpath("./following-sibling::a[1]")
        link = link_elem.get_attribute('href')
        break
driver.get(link)


driver.close()
driver.quit()







