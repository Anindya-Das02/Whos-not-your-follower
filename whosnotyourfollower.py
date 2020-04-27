from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup

"""
creator: Anindya Das
contact-email: anindya9809@gmail.com
twitter: @dasanindya98
"""

# checks for Notification pop-up
def modalPresent(driver):
    try:
        pop_up = driver.find_element_by_xpath("""/html/body/div[4]/div""")
        if(pop_up):
            return True
    except:
        pass
    return False

def wait(timeperiod = 5, sno = 'unknown'):
    print()
    print(f"sleep #{sno} for {timeperiod} sec...")
    sleep(timeperiod)
    print(f"woke up from sleep #{sno}")
    print()

# checks for incorrect credentials
# if incorrect return true else false
def checkForIncorrectAccountCredentials(driver):
	try:
		incorrect_cred = driver.find_element_by_xpath("""/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[7]""")
		if(incorrect_cred):
			return True
	except:
		pass
	return False


url = "https://www.instagram.com/"

print("*********** WHO'S NOT YOUR FOLLOWER? ***************")
print("please enter your instagram credentials below:")
username_ip = input("username/email/phn: ")
password_ip = input("password: ")

driver = webdriver.Chrome()
driver.get(url)
wait(5,1)
username = driver.find_element_by_xpath("""/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input""")
password = driver.find_element_by_xpath("""/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input""")
login_btn = driver.find_element_by_xpath("""/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button""")
username.send_keys(username_ip)
password.send_keys(password_ip)
login_btn.click()

wait(5,2.5)

#======================================
# checking for correct account details
# if account credentials wrong terminate the program
# else login
if(checkForIncorrectAccountCredentials(driver)):
	print("Woops, something looks wrong!")
	print("Incorrect Account credentials!")
	print("-- program terminated --")
	driver.close()
	exit(0)
#======================================

print("logining in...")

wait(5,2)

#======================================
# checking for two factor auth
# if so complete the process manually 
if('accounts/login/two_factor' in driver.current_url):
    print("two factor sign-in detected!")
    print("please complete this step manually!")
    print("waiting for two factor auth completion...")
    while(driver.current_url != 'https://www.instagram.com/'):
        print("waiting for completion..")
        sleep(3) 
    print("two factor process completed")
        
# two factor process completed
#======================================
wait(3,3)
print("logged in...")
#======================================
# checking for pop up [turn notificatio on]
# clicking 'not now' option
if(modalPresent(driver)):
    print("pop up visible")
    driver.find_element_by_xpath("""/html/body/div[4]/div/div/div[3]/button[2]""").click()
    print("notification pop up -> [not now] clicked")

# pop-up handler finish
#=====================================

driver.find_element_by_xpath("""/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/a""").click()
wait(5,4)
driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/header/section/ul/li[2]/a""").click()
wait(3,5)

#====================================
# fetching list of followers

print("fetching list of followers...")
print("please wait...")

curr_height = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].scrollHeight""")
while(True):
    driver.execute_script("""document.getElementsByClassName('isgrP')[0].scrollTo(0,document.getElementsByClassName('isgrP')[0].scrollHeight)""")
    sleep(5)
    new_height = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].scrollHeight""")
    if(new_height == curr_height):
        break
    curr_height = new_height

# end
#======================================
wait(3,6)

follower_res = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].outerHTML""")
driver.find_element_by_xpath("""/html/body/div[4]/div/div[1]/div/div[2]/button""").click()
wait(3,7)

#===================================
# fetching lost of following

driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/header/section/ul/li[3]/a""").click()
wait(3,8)
curr_height = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].scrollHeight""")

print("fetching your following data...")
print("please wait...")

while(True):
    driver.execute_script("""document.getElementsByClassName('isgrP')[0].scrollTo(0,document.getElementsByClassName('isgrP')[0].scrollHeight)""")
    sleep(5)
    new_height = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].scrollHeight""")
    if(new_height == curr_height):
        break
    curr_height = new_height
    
following_res = driver.execute_script("""return document.getElementsByClassName('isgrP')[0].outerHTML""")
driver.find_element_by_xpath("""/html/body/div[4]/div/div[1]/div/div[2]/button""").click()
wait(3,8)
print("fetching process finished!")

#=======================================
# web scraping starts

# extract the names/userids of the followers 
# and add them in a set
soup = BeautifulSoup(follower_res,'lxml')
followers_set = set()
followers_div = soup.findAll("li",{"class":"wo9IH"})
for fd in followers_div:
    try:
        fname = fd.find("a",{"class":"FPmhX"})
        #print(fname.text)
        followers_set.add(fname.text)
    except:
        pass

# extract the names/userids of the following 
# and add them in a set
soup2 = BeautifulSoup(following_res,'lxml')
following_set = set()
following_div = soup2.findAll("li");
for fwd in following_div:
    try:
        fwname = fwd.find("a",{"class":"FPmhX"})
        #print(fwname.text)
        following_set.add(fwname.text)
    except:
        pass

#==============================================
# final result
print("Account Summary:")
print(f"no. of follower: {len(followers_set)}")
print(f"no. of following: {len(following_set)}")
print()

if(len(followers_set ) > len(following_set)):
    print("wow! you have more followers than following!")
else:
    diff_set = following_set - followers_set
    diff_list = sorted(list(diff_set))
    print(f"{len(diff_list)} people who are not following you are:")
    for i in diff_list:
        print(f"\t{i}")

sleep(3)
driver.close()
print()
print("==== FIN ====")