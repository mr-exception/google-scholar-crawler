import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print("fetch single page script")

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87")

browser = webdriver.PhantomJS(executable_path='phantomjs/bin/phantomjs', desired_capabilities=dcap)

browser.get('https://scholar.google.com/scholar?start=20&q=oxygen&hl=en&as_sdt=0,5')
items = browser.find_elements_by_class_name('gs_ri')
for item in items:
    try:
        titleItem = item.find_element_by_class_name('gs_rt')
        title = titleItem.text
        link = titleItem.find_element_by_tag_name('a').get_attribute('href')
        
        print('link:  ' +link)
        print('title: ' + title) 
        print("==================================================================")
    except:
        print("# item is not castable")