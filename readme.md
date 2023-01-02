# Project Title

## Description
This project is webscraper that scrapes informaion about various jobs posted in a website called naukari.com

## Video Demo
https://youtu.be/4CbgnqJpsNo


## Project Structure


- project.py
- test_project.py
- requirements.txt
- README.md
- naukari.csv

## Libraries

- **Selenium:** Selenium is an open-source tool that automates web browsers
- **csv:** It presents classes and methods to perform read/write operations on CSV file as per recommendations of PEP 305
- **time:** The Python time module provides many ways of representing time in code, such as objects, numbers, and strings.
- **typing:** Typing defines a standard notation for Python function and variable type annotations.

## Functions

#### get_city_links
This function creates a WebDriver object and then uses it to get the links of all the locations present in the naukari.com and returns the list of said links

#### jobs_info
This function takes a list of links of locations present in naukari.com and iterates over them and  then iterates over each job present in that location and returns a Generator object contaning a dict object that contains the imformation regarding the jobs

#### file_creator
This function takes a Generator object containing dict and creates a csv file with the data present in the dict

#### file_name_checker
This function checks weather the of the file's extenction (csv) is correct or not