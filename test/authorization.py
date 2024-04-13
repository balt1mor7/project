from selenium.webdriver.common.by import By
from colorama import Fore, Style


def authorization(driver, domain):
    data = {
            'login': "user",
            'password': "user",
        }
    if not login(driver, domain, data):
        return False
    return True


def login(driver, domain, data):
    try:
        driver.get(f"{domain}/auth/login")
        input_username = driver.find_element(By.XPATH, "/html/body/main/div/form/div[1]/input")
        input_password = driver.find_element(By.XPATH, "/html/body/main/div/form/div[2]/input")
        input_username.send_keys(data['login'])
        input_password.send_keys(data['password'])
        driver.find_element(By.XPATH, "/html/body/main/div/form/button").click()
        if "Вы успешно аутентифицированы." in driver.find_element(By.XPATH, "/html/body/div[1]").text:
            print(Fore.GREEN, driver.find_element(By.XPATH, "/html/body/div[1]").text, Style.RESET_ALL, sep='')
            return True
        else:
            print(Fore.RED, "Аутентификация провалена :(", Style.RESET_ALL, sep='')
            return False
    except:
        print(Fore.RED,"ERROR:", Style.RESET_ALL, "Во время авторизации произошла ошибка!", sep='')
        return False


def logout(driver):
    try:
        driver.find_element(By.XPATH, "/html/body/header/nav/div/div/a").click()

        if "Вы вышли из своей учетной записи" in driver.find_element(By.XPATH, "/html/body/div[1]").text:
            print(Fore.GREEN, driver.find_element(By.XPATH, "/html/body/div[1]").text, Style.RESET_ALL)
            return True
        else:
            print(Fore.RED, "Выход провален :(", Style.RESET_ALL, sep='')
            return False
    except:
        print(Fore.RED,"ERROR:", Style.RESET_ALL, "Во время выхода произошла ошибка!", sep='')
        return False
