import random
import re
import ssl
from xml.etree import ElementTree

import requests
from lxml import etree
import pandas as pd
from tqdm import tqdm

import click


class Glassdoor(object):
    job_name = ""
    length_job_name = ""
    main_Web_url = ""

    my_headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.43",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"
    ]
    proxy_list = {
        'http': '50.206.25.105',
        'http': "50.206.25.108",
        'http': "108.29.77.74",
    }

    __main_Web_url_prefix = ""
    __main_Web_url_suffix = ".htm"
    __main_Web_url_other_pages = "_IP"

    def __init__(self, job_name):
        """
        Enter a string job name to init the GlassDoor
        :param job_name: A string job name
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        self.job_name = "-".join(job_name.split(" "))
        self.length_job_name = len(self.job_name)
        self.__main_Web_url_prefix = "https://www.glassdoor.com/Job/" + self.job_name + "-jobs-SRCH_KO0," + str(
            self.length_job_name)
        self.main_Web_url = self.__main_Web_url_prefix + self.__main_Web_url_suffix

    def build_etree(self, resp):
        """
        check the state code of the response object and return etree object
        :param resp: response object
        :return: etree object
        """
        html = ""
        # check the status code is 200
        if resp.status_code is requests.codes['ok']:
            html = etree.HTML(resp.content)
        else:
            print("Check website availability....", "Website status code is", resp.status_code)

        return html

    def build_request(self, url):
        resp = requests.get(url, headers={"user-agent": random.choice(self.my_headers)},
                            proxies=self.proxy_list)
        return resp

    def get_page_numbers(self):
        """
        Get the total page number result for current job
        :return: int
        """
        page_number = 0

        resp = self.build_request(self.main_Web_url)
        html = self.build_etree(resp)

        if html is not "":
            # check if the page number tag exist
            try:
                page_number = html.xpath('//*[@id="ResultsFooter"]/div[1]')[0]
                page_number = page_number.xpath('./text()')[0]
                page_number = page_number.split(" ")[-1]
            except:
                print("We find 0 page of result from this search")

        return int(page_number)

    def build_page_url(self, page_number):
        """
        Get all the page urls for current job
        :param page_number: string,int
        :return: list
        """
        page_urls = []
        if page_number != 0:
            for i in range(page_number):
                main_Web_url = self.__main_Web_url_prefix + self.__main_Web_url_other_pages + str(
                    i + 1) + self.__main_Web_url_suffix
                page_urls.append(main_Web_url)
        return page_urls

    def get_job_url(self, url):
        """
        Get all job url from the page url
        :param url: string
        :return: list
        """
        job_urls = []

        resp = self.build_request(self.main_Web_url)
        html = self.build_etree(resp)

        if html is not "":
            # check if the page number tag exist
            try:
                href = html.xpath('//*[@id="MainCol"]/div[1]/ul/li/div[1]/a')
                for el in href:
                    local_href = el.xpath('./@href')[0]
                    global_href = 'https://www.glassdoor.com' + local_href
                    job_urls.append(global_href)
            except:
                print("href is not find for current page", url)

        return job_urls

    def get_basic_information(self, url, **kwargs):
        """
        :param url: string
        :param kwargs: bool Company(default=True), Time(default=True),Location(default=True), Job_Name (default=True), Job_Type(default=True),
        Key_Word(default=[])
        :return: dataFrame
        """

        company = kwargs.get("Company", True)
        time = kwargs.get("Time", True)
        location = kwargs.get("Location", True)
        job_name = kwargs.get("Job_Name", True)
        job_type = kwargs.get("Job_Type", True)
        key_word = kwargs.get("Key_Word", [])

        df = pd.DataFrame()
        if isinstance(company, bool) and isinstance(time, bool) and isinstance(location, bool) and isinstance(
                job_type, bool) and isinstance(job_name, bool) and isinstance(key_word, list):

            information_dict = {"url": url}
            resp = self.build_request(url)
            e_html = self.build_etree(resp)
            data = resp.content
            try:
                div = e_html.xpath('//div[@class="desc css-58vpdc ecgq1xb4"]')[0]
                str_data = ElementTree.tostring(div, encoding='unicode')
            except:
                print("unable to find the keyword div the url is:", url)

            # str data for html
            html_str = str(data)

            if time:
                time = re.search(r'"datePosted": "(.+?)",', html_str)
                if time is not None:
                    time = time.group(0).split("\"")[-2]
                information_dict["time"] = time
            if company:
                try:
                    company = e_html.xpath('//div[@class="css-16nw49e e11nt52q1"]')[0]
                    company = company.xpath('./text()')[0]
                    information_dict["company"] = company
                except:
                    information_dict["company"] = "None"
            if location:
                try:
                    location = e_html.xpath(
                        '//div[@class="css-1v5elnn e11nt52q2"]')[0]
                    location = location.xpath('./text()')[0]
                    information_dict["location"] = location
                except:
                    information_dict["location"] = "None"
            if job_name:
                try:
                    job_name = e_html.xpath(
                        '//div[@class="css-17x2pwl e11nt52q6"]')[0]
                    job_name = job_name.xpath('./text()')[0]
                    information_dict["job_name"] = job_name
                except:
                    information_dict["job_name"] = "None"
            if job_type:
                job_type = re.search(r'"employmentType": "(.+?)"', html_str)
                if job_type is not None:
                    job_type = job_type.group(0).split("\"")[-2]
                information_dict["job_type"] = job_type
            if len(key_word) > 0:
                key_word_dict = {}
                for i in key_word:
                    word_exist_state = False
                    if re.search(i, str_data, re.IGNORECASE) is not None:
                        word_exist_state = True
                    key_word_dict[i] = word_exist_state
                information_dict["key_word"] = key_word_dict
            df = df.append(information_dict, ignore_index=True)

        return df

    def concat_df(self, df_total, df):
        """
        :param df_total: dataframe
        :param df: dataFrame
        :return: dataFrame
        """
        df_total = df_total.append(df)

        return df_total

    def get_csv(self, df, file_name):
        """
        :param df:
        :param file_name:
        :return:
        """

        # remove the duplicates in the data set
        # I don't know why there is duplicate in the data set
        if df != 0:
            df = df.drop_duplicates(subset=["url"])
            df = df.reset_index(drop=True)
            df.to_csv(file_name)

    def run(self, file_name, **kwargs):

        company = kwargs.get("Company", True)
        time = kwargs.get("Time", True)
        location = kwargs.get("Location", True)
        job_name = kwargs.get("Job_Name", True)
        job_type = kwargs.get("Job_Type", True)
        key_word = kwargs.get("Key_Word", [])

        df = pd.DataFrame()
        if isinstance(company, bool) and isinstance(time, bool) and isinstance(location, bool) and isinstance(
                job_type, bool) and isinstance(job_name, bool) and isinstance(key_word, list):
            job_url_t = []
            page_number = self.get_page_numbers()
            page_urls = self.build_page_url(page_number)
            df_total = 0
            print("We have found", len(page_urls), "pages of results from the search of", self.job_name)
            for url in tqdm(page_urls):
                job_url = self.get_job_url(url)
                job_url_t.extend(job_url)
            print("We have found", len(job_url_t), "results from the search of", self.job_name)
            for url in tqdm(job_url_t):
                df = self.get_basic_information(url, Company=company, Time=time, Location=location, Job_Name=job_name,
                                                Job_Type=job_type, Key_word=key_word)
                df_total = self.concat_df(df_total, df)

        self.get_csv(df_total, file_name)
