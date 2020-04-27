# Whos-not-your-follower

It is annoying when people first follow you on ```Instagram``` and then suddenly unfollow you while you are still following them. It is hard to see who has unfollowed when you have hundreds or thousands of followers and followings. This program helps you to do that exactly.  

This program uses ```web scraping``` to do that. Run the program, enter your instagram username and password in the CLI. The programm opens your instagram account in a browser and scrapes information from it.  

In the end, the program lists out all the ```user ids``` who do not follow you back.

## In case of two factor authentication
Even though the entire web scraping is fully automated. But if your account is protected through two factor authentication you need to complete the process manually. Enter the security code in the browser and continue. The rest of the process continues automatically.


# Requirements / Dependencies
* python version above ```3.6```
* selenium
  ```
  > pip install selenium
  ```
* Chrome webdriver [ [download-link](https://chromedriver.chromium.org/) ]
* beautifulsoup4
  ```
  > pip install beautifulsoup4
  ```
* requests
  ```
  > pip install requests
  ```
* lxml
  ```
  > pip install lxml
  ```

