from bs4 import BeautifulSoup
import string
import requests
import os


class WebScraper:
    def __init__(self):
        self.url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
        self.number_of_pages = int(input())
        self.type_of_article = input()
        self.current_directory = os.getcwd()

    def main(self):
        self.create_folders()
        self.send_request()

    def send_request(self):
        counter = 1

        request = requests.get(self.url, headers={"Accept-Language": "en-US,en;q=0.5"})
        soap = BeautifulSoup(request.content, "html.parser")

        for i in soap.find_all("article"):
            for j in i.find_all("span"):
                if j.text == self.type_of_article and counter <= self.number_of_pages:
                    file_name = i.find('a').text.strip().replace(' ', '_').strip(string.punctuation).replace('’', '')

                    with open(f"{self.current_directory + '/Page_' + str(counter) + '/' + file_name}.txt",
                              "wb") as file:
                        soup = BeautifulSoup(requests.get("https://www.nature.com" + i.find("a").attrs["href"] +
                                                          "/", headers={"Accept-Language": "en-US,en;q=0.5"})
                                             .content, "html.parser")

                        file.write(soup.find('div', {'class': 'c-article-body u-clearfix'}).text.
                                   encode(encoding='utf-8'))

                    counter += 1

    def create_folders(self):
        for i in range(1, self.number_of_pages + 1):
            os.mkdir(self.current_directory + "/Page_" + str(i))
            os.chdir(self.current_directory)


if "__main__" == __name__:
    WebScraper().main()
