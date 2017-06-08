from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from time import sleep


class QinxinParser(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "http://www.qixin.com/"
        self.driver.get(self.url)
        sleep(15)
        

    def parse_qixin(self,data):
        if data['Company_name']=="暂未收录":
            data['Company_type'] = "无记录"
            data['Legal_representative'] = "无记录"
            data['Establishment_data'] = "无记录"
            data['TIB_adress'] = "无记录"
            data['Business_scope'] = "无记录"
            data['Contact_phone'] = '无记录'
            data['E-mail'] = '无记录'
            return data
      
        #sleep(1)
        #el = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/form/div[1]/span[1]/input[2]")
        #el1 = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/form/div[1]/span[1]/input[1]")
        #print (data['Company_name'])
        #sleep(1)
        #el.send_keys(data['Company_name'])
        #el1.send_keys(data['Company_name'])

        #self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/form/div[1]/span[2]").click()

        #sleep(1)

        Company_key = urllib.request.quote(data['Company_name'])
        self.driver.get('http://www.qixin.com/search?key='+ Company_key +'&type=enterprise&method=all')
        sleep(1)
        html = self.driver.page_source

        soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')
        try:
            node = soup.find('div',class_ ="search-result-desc").find('a')
        except:
            data['Company_type'] = "无记录"
            data['Legal_representative'] = "无记录"
            data['Establishment_data'] = "无记录"
            data['TIB_adress'] = "无记录"
            data['Business_scope'] = "无记录"
            data['Contact_phone'] = '无记录'
            data['E-mail'] = '无记录'
            self.driver.get(self.url)
            return data
        


        old_url = 'http://www.qixin.com/'
        new_url = node['href']
        new_full_url = urllib.parse.urljoin(old_url,new_url)


        self.driver.get(new_full_url)

        sleep(1)

        #html = driver.page_source

        #soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')

        #node = soup.find_all('div',class_='col-xs-6')

        #data['Company_type'] = node[2].find('span').get_text()

        
        data['Company_type'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/span").text
        data['Legal_representative'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]/a").text
        data['Establishment_data'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/span").text
        data['TIB_adress'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/span").text
        data['Business_scope'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[1]/div[1]/span").text


        html = self.driver.page_source
        soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')

        

        if soup.find('a',href='#report'):
            self.driver.get(new_full_url+'#/report')
            sleep(1)
            self.driver.refresh()
            sleep(2)
            data['Contact_phone'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[6]/div[1]/div[2]/div[2]/div[2]/div[1]/span").text
            data['E-mail'] = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[4]/div[1]/div[1]/div[1]/div[6]/div[1]/div[2]/div[2]/div[4]/div[1]/span").text
        else:
            data['Contact_phone'] = '无记录'
            data['E-mail'] = '无记录'

        #self.driver.get(self.url)

        return data













        #print (data)

        #driver.
