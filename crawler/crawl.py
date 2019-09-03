from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_file_contents(browser, script):
    browser.execute_script(script)

    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "pre"))
    )

    file_contents = element.get_attribute("innerHTML")

    browser.back()
    return file_contents


display = Display(visible=0, size=(1366, 768))
display.start()

browser = webdriver.Firefox(executable_path=r'driver/geckodriver', log_path='/tmp/geckodriver.log')
browser.get('http://www.onefilmes.com.br/contato/#')

for el in browser.find_elements_by_tag_name("a"):
    script_name = el.get_attribute("onclick")

    if script_name is None:
        # Not all a tags have an onclick attribute...
        continue

    if script_name.find('FilesMan') > 0:
        # It's a directory...
        part = script_name.split('\'')
        if len(part) > 1:
            print("Dir name: ", part[3])
    elif script_name.find('view') > 0:
        # It's a file....
        print("File name: ", script_name.split('\'')[3])
        # get_file_contents(browser, script_name)

browser.quit()
display.stop()
