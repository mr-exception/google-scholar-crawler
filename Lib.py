import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

browser = driver = webdriver.Chrome('chrome/chromedriver-2.26')
#   ================================      step 0      ==================================
def login(username, password):
    browser.get("https://accounts.google.com")
    browser.find_element_by_id("Email").send_keys(username)
    browser.find_element_by_id("next").click()
    time.sleep(1)
    browser.find_element_by_id("Passwd").send_keys(password)
    browser.find_element_by_id("signIn").click()
    browser.get("https://scholar.google.com")

#   ================================      step 1      ==================================
def saveAllArticlesInPage():
    saveItems = browser.find_elements_by_xpath('//*[contains(@id, "gs_svl")]')
    print("got " + str(len(saveItems)) + " articles")
    for item in saveItems:
        functionString = item.get_attribute('onclick')[7:]
        browser.execute_script(functionString)

def openSearch(searchIndex, pageNumber=0):
    start = pageNumber * 20
    browser.get('https://scholar.google.com/scholar?start=' + str(start) + '&q=' + searchIndex + '&hl=en&as_sdt=0,5')

def startSaveingArticles(searchIndex, count=100):
    for pageNumber in range(0, int(count/20)):
        openSearch(searchIndex, pageNumber)
        saveAllArticlesInPage()

#   ================================      step 2      ==================================
def getLibraryArticleLinks():
    browser.get("https://scholar.google.com/scholar?start=0&hl=en&as_sdt=0,5&scilib=1")
    
    linkArray = []
    offset = 0
    
    while(getArticlesLinksSinglePage(linkArray) == 1):
        offset += 10
        browser.get("https://scholar.google.com/scholar?start=" + str(offset) + "&hl=en&as_sdt=0,5&scilib=1")

    return linkArray

def getArticlesLinksSinglePage(linkArray):
    items = browser.find_elements_by_xpath('//a[contains(@href, "/citations?view_op=view_citation&continue=/scholar")]')
    if(len(items) == 0):
        return 0
    for item in items:
        linkArray.append(item.get_attribute('href'))

    return 1
#   ================================      step 3      ==================================
def getArticleInfoFromCitationLink(link):
    browser.get(link)

    result = {}
    result['title'] = browser.find_element_by_class_name('gsc_title_link').text
    result['pageLink'] = browser.find_element_by_class_name('gsc_title_link').get_attribute('href')

    pdfLinks = browser.find_elements_by_class_name('gsc_title_ggi')
    if len(pdfLinks) > 0:
        result['pdfLink'] = pdfLinks[0].find_element_by_xpath('//a').get_attribute('href')

    fields = browser.find_elements_by_class_name('gs_scl')
    for field in fields:
        key = field.find_element_by_class_name('gsc_field').text
        value = field.find_element_by_class_name('gsc_value')
        if key == 'Authors':
            result['authors'] = value.text.split(" ,")
        elif key == 'Publication date':
            result['pub-date'] = value.text
        elif key == 'Description':
            result['description'] = value.text.replace("\n", " ")
        elif key == 'Journal':
            result['journal'] = value.text
        elif key == 'Volume':
            result['volume'] = value.text
        elif key == 'Issue':
            result['issue'] = value.text
        elif key == 'Pages':
            result['pages'] = value.text
        elif key == 'Publisher':
            result['publisher'] = value.text
        elif key == 'Total citations':
            result['citationsLink'] = value.find_element_by_xpath('//a').get_attribute('href')
    return result

def getArticleInfoList(linkArray):
    result = []

    count = 0
    total = len(linkArray)
    
    for link in linkArray:
        info = getArticleInfoFromCitationLink(link)
        result.append(info)

        count += 1
        print(str(count/total) + " %")

    return result

def saveArticleInfo(infoList, fileName):
    file = open('files/' + fileName + '.json', 'w')
    file.write(str(infoList))
    file.close()
    print("saved info in " + 'files/' + fileName + '.json')
#   ================================      step 4      ==================================
def removeArticlesFromLibrary():
    browser.get("https://scholar.google.com/scholar?start=0&hl=en&as_sdt=0,5&scilib=1")
    print("removing from library")
    count = 0
    while(True):
        try:
            browser.find_element_by_id("gs_ab_x_all").click()
            browser.find_element_by_id("gs_ab_del").click()
            count += 20
            print("removed " + str(count) + " articles")
        except:
            print("removed " + str(count) + " articles from my library")
            break

def remvoeForEver():
    browser.get("https://scholar.google.com/scholar?hl=en&num=20&as_sdt=0,5&scilib=3")
    count = 0
    while(True):
        try:
            browser.find_element_by_id("gs_ab_x_all").click()
            browser.find_element_by_id("gs_ab_del_fevr").click()
            count += 20
            print("removed " + str(count) + " articles")
        except:
            print("removed " + str(count) + " articles from my library")
            break
#   ================================      step 4      ==================================
def completedProgress(searchIndex, articleCount=100):
    startSaveingArticles(searchIndex, articleCount)
    linkArray = getLibraryArticleLinks()
    authorList = getArticleInfoList()
    saveArticleInfo(authorList, searchIndex)
    removeArticlesFromLibrary()
    remvoeForEver()

login("bidelsorkh", "ad2yesh1996")
print("imported ex Lib")