import boto3
import time, hashlib
from selenium import webdriver


def get_screenshot(URL, browser = 'chrome', widths = [360, 768, 1920]):
    
    if browser == 'chrome':
        #Initializing headless Chrome webdriver
        options = webdriver.ChromeOptions()
        options.headless = True
        browser = webdriver.Chrome(options = options, executable_path = "./chromedriver")

    elif browser == 'firefox':
        #Initializing headless Firefox webdriver
        ffox_options = webdriver.FirefoxOptions()
        ffox_options.headless = True
        browser = webdriver.Firefox(executable_path = './geckodriver', options = ffox_options)

    try:
        start = time.time()
        print('Connecting to:', URL)
        browser.get(URL)
        time.sleep(1)
        S = lambda X: browser.execute_script('return document.body.parentNode.scroll'+X)

        for width in widths:
            # Filename encoding to be checked
            filename = hashlib.md5(URL.encode()).hexdigest() + '_' + str(width) + '.png'

            browser.set_window_size(width, width)
            time.sleep(2)    
            browser.set_window_size(width, S('Height'))
            time.sleep(2)                                                                                                             
            browser.find_element_by_tag_name('body').screenshot('runtime/'+filename)
            print(width, 'screenshot OK')
        
        print('Total time:', round(time.time() - start, 1), 'seconds')

    except:
        print('Unable to connect!\n')
    finally:
        browser.quit()


def upload_screenshot(file_name, bucket, remote_name=None):
    if remote_name == None:
        remote_name = file_name 
    # Upload the file
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, remote_name)

if __name__ == '__main__':
    get_screenshot(URL = 'http://www.w3schools.com/js/default.asp', browser='chrome')