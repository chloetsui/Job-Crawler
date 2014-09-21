#!/usr/bin/env python
#! -*-coding:utf8-*-

import re
import urllib2

from bs4 import BeautifulSoup


class Job(object):

    def __init__(self, id, title, company):
        self.id = id
        self.title = title
        self.company = company


class Spider(object):
    ROOT_URL = "http://www.indeed.com/jobs?q={job}&l={zipcode}&start={start}"
    
    def __init__(self, job, zipcode, count):
        self.urls = [self.ROOT_URL.format(job=job, zipcode=zipcode, start=page_num*10) for page_num in range(count)]
        self.job_list = []

    def run(self):
        for i, url in enumerate(self.urls):
            print 'Crawling the page {num}.'.format(num=i)
            content = self.fetch_content(url)
            self.job_list += self.parse_content(content)
        self.display_jobs()

    def fetch_content(self, url):
        html = urllib2.urlopen(url).read()
        return html

    def parse_content(self, content):
        job_list = []
        soup = BeautifulSoup(content)
        for row in soup.find_all('div', 'row'):
            job_id = row.h2['id']
            job_title = row.h2.a['title']
            company = row.span.span.string
            job_list.append(Job(job_id, job_title, company))
        return job_list

    def display_jobs(self):
        print "{count} jobs crawled.".format(count=len(self.job_list))
        for job in self.job_list:
            print job.company, job.title

def main():
    s = Spider("Data Analyst", 10027, 3)
    s.run()

if __name__ == '__main__':
    main()
