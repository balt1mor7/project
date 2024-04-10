from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utilities import phase
from authorization import authorization, logout

from time import sleep

def auto_test():
   options = webdriver.ChromeOptions()

   options.add_argument("start-maximized")
   options.add_argument("disable-infobars")
   options.add_argument("--disable-extensions")
   options.add_argument("--disable-gpu")
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument("--no-sandbox")

   driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="123.0.6312.106").install()), options=options)
   driver.implicitly_wait(10)
   
   domain = "http://127.0.0.1:80"

   driver.get(domain)

   phase(1, "Тестирование авторизации")
   result_authorization = authorization(driver, domain)
   assert result_authorization == True, "Ошибка модуле авторизации."

   driver.close()
   driver.quit()

def main():
   auto_test()
   print('\n\n\n')

main()
