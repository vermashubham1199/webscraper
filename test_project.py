from project import get_city_links, jobs_info, NAUKARI_MAIN, file_creator
import csv
import os

list_of_dict = [{"test1":"testing1", "test2":"testing2", "test3":"testing3"}]

def test_get_link():
    get_city_links(NAUKARI_MAIN)

def test_job_info():
    jobs_info(
        [
            'https://www.naukri.com/jobs-in-mumbai',
    'https://www.naukri.com/jobs-in-bangalore',
    'https://www.naukri.com/jobs-in-delhi',
    'https://www.naukri.com/jobs-in-gurgaon',
    'https://www.naukri.com/jobs-in-noida',
    'https://www.naukri.com/jobs-in-chennai',
    'https://www.naukri.com/jobs-in-pune',
    'https://www.naukri.com/jobs-in-hyderabad-secunderabad',
    'https://www.naukri.com/jobs-in-kolkata',
    'https://www.naukri.com/jobs-in-ahmedabad',
    'https://www.naukri.com/jobs-in-chandigarh'
    ])

def test_csv():
    file_creator(list_of_dict, "testing.csv")

    with open("testing.csv", "r") as file:
        reader = csv.DictReader(file)
        for csv_row, job_row in zip(reader,list_of_dict):
            assert csv_row["test1"] == job_row["test1"]
            assert csv_row["test2"] == job_row["test2"]
            assert csv_row["test3"] == job_row["test3"]
    os.remove("testing.csv")