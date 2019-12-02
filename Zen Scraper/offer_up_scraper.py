
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from xlwt import Workbook 

wb = Workbook() 
offer_up_sheet = wb.add_sheet('Offer Up') 


driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
driver.get("http://www.offerup.com")

search = driver.find_element_by_css_selector('._dy79rkt._np351i')
search.send_keys('textbooks')

location = driver.find_element_by_css_selector('._dy79rkt._1kq0tk8')
location.clear()
location.send_keys('07302')

go = driver.find_element_by_class_name('_1ad1z4y')
go.click()

results = driver.find_elements_by_css_selector('._109rpto._1anrh0x')
handles = driver.window_handles

main_window = driver.current_window_handle
prices = driver.find_elements_by_class_name("_s3g03e4")
header_desc = None

book_prices = []
book_names = []
book_counter = 0

def get_book_price(book_count):
	price_counter = 0
	for price in prices:
		price_counter = price_counter + 1
		price_tuple = (price_counter, price.text)
		if book_count in price_tuple:
			return price_tuple

for link in results:
	book_counter = book_counter + 1
	book_price = get_book_price(book_counter)
		
	try:	
		link.send_keys(Keys.CONTROL	+ Keys.ENTER)
	except Exception as err:
		print("THE FOLLOWING ERROR HAS OCCURED {}".format(err))

	cur_win = [i for i in driver.window_handles]
	driver.switch_to_window(cur_win[-1])

	try:
		has_shipping = driver.find_element_by_css_selector('._1v68mn6s._17axpax')
		header_desc = driver.find_element_by_css_selector('._t1q67t0._1juw1gq').text
		offer_up_sheet.write(book_counter, 0, str((header_desc, book_price[1])))
		book_names.append((header_desc, book_price[1]))
	except Exception as err:
		print("ERROR {}".format(err), err)
	driver.switch_to_window(main_window)
	wb.save('book_leads.xls') 



