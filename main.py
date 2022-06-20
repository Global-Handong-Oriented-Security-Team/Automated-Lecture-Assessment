"""
Writer: 김진일
Date: 2022.6.18
""" 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == '__main__': 
    chromedriver_path = input("Enter a chromedriver path: ")
    hisnet_id = input("Enter a hisnet id: ") 
    hisnet_pw = input("Enter a hisnet password: ")

    driver = webdriver.Chrome('/Users/jinil/Desktop/LectureAssessment/chromedriver')
    driver.implicitly_wait(3)

    # Open the site 
    driver.get('https://hisnet.handong.edu/login/login.php')

    # Enter the ID and PW
    username = driver.find_element(By.NAME, 'id')
    username.send_keys(hisnet_id) 

    password = driver.find_element(By.NAME, 'password')
    password.send_keys(hisnet_pw) 

    # Click login button 
    driver.find_element(By.XPATH, "/html/body/div[1]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input").click()

    # Open assessment page
    driver.get('https://hisnet.handong.edu/for_student/course/HLES150M.php') 

    # Find assessment lists
    assess_table = driver.find_element(By.XPATH, "/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody")
    assess_list = assess_table.find_elements(By.TAG_NAME, 'tr') 
    
    lecture_names = [ ]
    lecture_assess_links = [ ]
    num_of_lectures = -1 
    
    # Get assessment lists
    for lecture in assess_list:
        if num_of_lectures != -1:
            
            # Append lecture name
            td = lecture.text.split(' ')
            lecture_names.append(td[2])

            # Append Assessment Link
            if len(lecture.find_elements(By.TAG_NAME, 'a')) > 0: 
                lecture_assess_links.append(lecture.find_element(By.TAG_NAME, 'a').get_attribute("href")) 

        num_of_lectures = num_of_lectures + 1

    # Print the lecture name and link 
    for lecture_name, link in zip(lecture_names, lecture_assess_links):
        print(lecture_name + " : " + link)

    # Access the link 

    for name, link in zip(lecture_names, lecture_assess_links): 
        driver.get(link)
        driver.maximize_window()

        real_assess_table = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/form/table[3]/tbody')
        a_list = real_assess_table.find_elements(By.TAG_NAME, 'tr') 

        assess_count = -1 
        # Click 5 point element 
        for tr in a_list: 
            if assess_count != -1 : 
                input_tag = tr.find_element(By.TAG_NAME, 'input')
                if input_tag.get_attribute('type') == 'radio': 
                    input_tag.click()
            assess_count = assess_count + 1

        driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/form/table[4]/tbody/tr/td/a').click()

        print('The \''+name+'\' lecture assessment is done!')

        driver.switch_to.alert.accept()
        time.sleep(1)

    print("All is done!")
