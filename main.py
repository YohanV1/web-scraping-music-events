import requests
import selectorlib
import time
import sqlite3
from send_email import send_email

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("webscrapingtours.db")


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    # with open("data.txt", 'a') as file:
    #     file.write(extracted + "\n")
    extracted_list = extracted.split(',')
    extracted_list = [data.strip() for data in extracted_list]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", extracted_list)
    connection.commit()


def read():
    # with open("data.txt", 'r') as file:
    #     return file.read()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        if extracted != "No upcoming tours":
            content = read()
            extracted_list = extracted.split(',')
            extracted_tup = tuple([data.strip() for data in extracted_list])
            if extracted_tup not in content:
                store(extracted)
                send_email(extracted)
        time.sleep(2)


