import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time

with open('src\\cei.json', 'r') as json_file:
    cei_login = json.load(json_file)

brokers = []

keys = webdriver.common.keys.Keys
extFiles = os.getcwd() + r"\\src\\python\\ExtFiles"
prefs = {"download.default_directory": extFiles}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='F:/Projetos Python/cei-ext-import/src/python/chromedriver/chromedriver.exe',
                          chrome_options=options)


def open_browser():
    driver.get('https://cei.b3.com.br/CEI_Responsivo/')
    driver.execute_script('window.name ="cei";')


def login_cei():
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtLogin').send_keys(cei_login['login'])
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtSenha').send_keys(cei_login['password'], keys.ENTER)


def login_cei_successful():
    while driver.current_url == 'https://cei.b3.com.br/CEI_Responsivo/':
        pass
    print('login successful')


def goto_extracts():
    driver.get('https://cei.b3.com.br/CEI_Responsivo/extrato-bmfbovespa.aspx')
    print('on extracts')


def get_brokers():
    brokers_dropdown = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))
    for option in brokers_dropdown.options:
        brokers.append(option.text)
        print(brokers)


def select_broker(broker):
    brokers_dropdown = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))
    brokers_dropdown.select_by_visible_text(broker)
    time.sleep(10)


def download_all_avaliable_extracts():
    extracts_dropdown = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlFiltroMes'))

    extracts_dropdown_opt_text = []

    for option in extracts_dropdown.options:
        extracts_dropdown_opt_text.append(option.text)

    print(extracts_dropdown_opt_text)
    for option in extracts_dropdown_opt_text:
        btn_excel_download = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnVersaoEXCEL')
        print(option)
        extracts_dropdown.select_by_visible_text(option)
        btn_excel_download.click()
        print('mounth: ' + option)
        download_wait(extFiles, 180)
        extracts_dropdown = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlFiltroMes'))


def download_wait(directory, timeout):
    seconds = 0
    dl_wait = True
    files = os.listdir(directory)
    count_files = len(files)
    while dl_wait and seconds < timeout:
        time.sleep(1)
        files = os.listdir(directory)
        lenFiles = len(files)
        if count_files < lenFiles:
            dl_wait = False
        print(seconds)
        seconds += 1


if __name__ == '__main__':
    open_browser()
    login_cei()
    login_cei_successful()
    goto_extracts()
    get_brokers()
    select_broker(brokers[2])
    download_all_avaliable_extracts()
    driver.quit()
