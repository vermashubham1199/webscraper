from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from typing import List, Callable, Optional, Any, Sequence, Generator 
from selenium.common.exceptions import NoSuchElementException, WebDriverException,InvalidSessionIdException
import csv
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service


COMP_NAME = "/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[1]/div/a"
EXP_REQ = "/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[1]/span"
CITY_XPATH = "/html/body/div[4]/div/div[1]/div/a"
COOKI_BUTTON = "/html/body/div[1]/div[4]/div[2]/div/button"
JOB_BUTTON = "/html/body/div[@id='root']/div[@class='search-result-container']/div[@class='search-result-wrap']/div[@class='content']/section[@class='listContainer fleft']/div[@class='list']/article[@class='jobTuple']/div[@class='jobTupleHeader']/div[@class='info fleft']/a"
NEXT_BUTTON = "//a[@class='fright fs14 btn-secondary br2']"
NAUKARI_MAIN = "https://www.naukri.com/jobs-by-location"
SALARY = "/html/body/div[1]/main/div[2]/div[2]/section[1]/div[1]/div[2]/div[2]/span"
DETAILS = "/html/body/div[@id='root']/main/div[@class='jd-container']/div[@class='leftSec']/section[@class='job-desc']/div[@class='other-details']/div[@class='details']/span/a[@target='_blank']"
DETAILS2 = "/html/body/div[@id='root']/main/div[@class='jd-container']/div[@class='leftSec']/section[@class='job-desc']/div[@class='other-details']/div[@class='details']/span"
ALERT_XPATH = "/html/body/div[1]/div[4]/div[2]/div/button"





def main():
    file_name = file_name_checker(input("Name of the file: "))
    no_of_pages = input("How many pages do you want ot iterate over: ")
    print(no_of_pages)
    if no_of_pages:
        file_creator(jobs_info(get_city_links(NAUKARI_MAIN), int(no_of_pages)), file_name)
    else:
        file_creator(jobs_info(get_city_links(NAUKARI_MAIN)), file_name)




def get_city_links(main_link: str) -> list[str]:
    """
    returns a list of links of all the top job locations in the naukari.com

    This function creates a webdriver object and then uses it to get the links of all the locations
    present in the naukari.com and returns the list of said links

    :param str main_link: link of the naukari.com
    :return list: links of all the links of the locations present 
    """



    service_driver = Service(executable_path=ChromeDriverManager().install())
    driver: WebDriver = webdriver.Chrome(service=service_driver) #this function download or update selenium chrome driver and sets it's path 
    driver.maximize_window()
    driver.get(main_link)
    driver.implicitly_wait(15)
    
    cities = driver.find_elements(By.XPATH, CITY_XPATH)
    return [city.get_attribute("href") for city in cities]








def jobs_info(job_links: list[str], pages: Optional[int]=10)-> Generator[dict, list[str], None]:
    """
    returns all the required information from each job in naukari.com

    This function takes a list of links of locations present in nakuri.com and iterates over them and  then 
    iterates over each job present in that location and returns a Generator object contaning a dict object that contains 
    the imformation regarding the jobs


    :param list job_links: list of all the links of locations present in the naukari.com
    :param int pages: a number of how many pages that the user want to iterate over
    :return Generator: information regarding the jobs 
    :exception: it ignores all those pages which are not from naukari.com but instead of the company that posted the job
    """
    




    # itreating over the links of cities
    for job_link in job_links:


        # Creating webdriver instance
        service_driver = Service(executable_path=ChromeDriverManager().install())
        driver: WebDriver = webdriver.Chrome(service=service_driver)
        driver.maximize_window()


        # opening each city link
        driver.get(job_link)
        driver.implicitly_wait(10)



        # handling cookie alert
        driver.find_element(By.XPATH,COOKI_BUTTON).click()


        time.sleep(3)
        # itreating over next buton 
        for i in range(pages):

            time.sleep(2)

            # itreating over each job of a city
            for job in driver.find_elements(By.XPATH,JOB_BUTTON):
                
                parent_window = driver.current_window_handle
                job.click()
                windos = driver.window_handles
                
                for i in windos:
                    if i != parent_window:
                        driver.switch_to.window(i)
                try:
                    comp_name = driver.find_element(By.XPATH, COMP_NAME ).text
                    experince_req = driver.find_element(By.XPATH, EXP_REQ ).text
                    salary = driver.find_element(By.XPATH, SALARY).text
                    detalis = driver.find_elements(By.XPATH, DETAILS)
                    details2 = driver.find_elements(By.XPATH, DETAILS2)



                except (NoSuchElementException, WebDriverException,InvalidSessionIdException):
                    pass

                else:
                    if detalis:
                        role = detalis[0].text
                        industry_type = detalis[1].text
                        functional_area = [i.text for i in  detalis[2:]]
                        functional_area = ",".join(functional_area)
                    if details2:
                        employment_type = details2[-2].text
                        role_category = details2[-1].text

                    yield{
                        "Company_name":comp_name,
                        "Experince_required":experince_req,
                        "Salary":salary,
                        "Role":role,
                        "Industry_type":industry_type,
                        "Functional_area":functional_area,
                        "Employment_type":employment_type,
                        "Role_category":role_category
                    }
                
                driver.close()
                driver.switch_to.window(parent_window)

            # clicking next button
            driver.find_element(By.XPATH,NEXT_BUTTON).click()
                
        driver.quit()





def file_creator(file: Generator[dict, list[str], None], name: str)-> None:
    """
    Takes a Generator object containing dict and creates a csv file with that information

    :param Generator file: a Generator object contaning dict objects
    :param str name: a str object to name the file that the  function creates
    :returns: None
    """




    for i in file:
        csv_keys = i.keys()
        break

    with open(name, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, csv_keys)
        dict_writer.writeheader()
        dict_writer.writerows(file)


def file_name_checker(name:str)-> str:
    """
    This function checks weather the of the file's extenction (csv) is correct or not
    

    :param str name: name of the file
    :returns str: correct name with propper extenction 
    """


    name = name.strip()
    if name.endswith(".csv"):
        return name
    else:
        return name+".csv"




if __name__ == "__main__":
    main()

