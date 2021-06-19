import time
from random import randint
from selenium import webdriver

def auto_comment(user_account, user_password, event_page, friend_count):
    driver = webdriver.Chrome(".\chromedriver.exe")
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    account = driver.find_element_by_name("username")
    account.clear() 
    account.send_keys(user_account)
    time.sleep(2)
    password = driver.find_element_by_name("password")
    password.send_keys(user_password)
    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
    login.click()
    time.sleep(5)
    notification = driver.find_element_by_class_name("cmbtv")
    notification.click()
    time.sleep(5)
    notification2 = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
    notification2.click()
    driver.get(f"https://www.instagram.com/{user_account}/")
    time.sleep(5)
    follower = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    follower.click()
    time.sleep(5)

    all_follower = []
    for i in range(1, friend_count+1):
        scr1 = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)
        driver.execute_script("arguments[0].scrollIntoView();", scr1)
        time.sleep(1)
        text = scr1.text
        all_follower.append(text.split("\n")[0])
    
    check = False
    while not check:
        print(all_follower)
        print("這些帳號裡面有哪些是不想標註的嗎?請以斜線隔開 e.g. xxx/yyy")
        without_account = input().split("/")
        for account in without_account:
            if account in all_follower:
                all_follower.remove(account)
        print("更新後帳號:")
        print(all_follower)
        print("是否正確:y ; 新增刪除帳號:n")
        answer = input()
        if answer.lower() == "y":
            check = True
            
    location = {0:"去吃拉麵",
               1:"去咖啡廳",
               2:"去圖書館",
               3:"去你家",
               4:"去酒吧"}
    
    for follower in all_follower:
        driver.get(event_page)
        time.sleep(5)
        commentArea = driver.find_element_by_class_name('Ypffh')
        commentArea.click()
        time.sleep(5)
        commentArea = driver.find_element_by_class_name('Ypffh')
        commentArea.click()
        commentArea.send_keys(f"@{follower} {location[randint(0, 4)]}")
        time.sleep(2)
        submit = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]')
        submit.click()

if __name__ == "__main__":
    print("請輸入帳號")
    user_account = input()
    print("請輸入密碼")
    user_password = input()
    print("請輸入活動網址")
    event_page = input()
    print("想要標記幾個朋友 ? (不得超過粉絲人數)")
    friend_count = int(input())
    auto_comment(user_account, user_password, event_page, friend_count)