from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse
from time import sleep
import re

#class WhoisParser(object):
#    def __init__(self):
#        self.driver = webdriver.Chrome()
#        self.url = "http://whois.chinaz.com/"
#        self.driver.get(self.url)
#        sleep(15)
class WhoisParser(object):
    def __init__(self):    
        self.driver = webdriver.Chrome()
        self.url = "http://whois.chinaz.com/"
        self.driver.get(self.url)
#data = {}
#以上为__init__

    def parse_whois(self,data):

        if data['Project_site'] == 'http://暂无' or data['Project_site'] == '无记录' or data['Project_site'] == 'http://无':
            data['Registrant_phone'] = '无记录'
            data['Registrant_Email'] = '无记录'
            data['Admin_phone'] = '无记录'
            data['Admin_Email'] = '无记录'
            return data
        self.driver.get('http://whois.chinaz.com/'+data['Project_site'][7:])
        #self.driver.refresh()
        #input_ = self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/form[1]/div[1]/span/input")
        #print (data['Project_site'])
        #input_.send_keys(data['Project_site'])
        #sleep(1)
        #input_.submit()
        #sleep(2)

        try:
            cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[8]/p").text
        except:
            try:
                cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[9]/p").text
            except:
                try:
                    cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[10]/p").text
                except:
                    try:
                        cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[11]/p").text
                    except:
                        try:
                            cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[12]/p").text
                        except:
                            cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[13]/p").text
        if re.match('Domain Name:',cont):
            try:
                data['Registrant_phone'] = re.search(r'Registrant Phone: +(.*)', cont).group(1)
            except:
                data['Registrant_phone'] = '无记录'
            try:
                data['Registrant_Email'] = re.search(r'Registrant Email: (.*)', cont).group(1)
                if '[' in data['Registrant_Email']:
                    data['Registrant_Email'] = data['Registrant_Email'][:-9:]
            except:
                data['Registrant_Email'] = '无记录' 
            try:
                data['Admin_phone'] = re.search(r'Admin Phone: +(.*)', cont).group(1)
            except:
                data['Admin_phone'] = '无记录'        
            try:
                data['Admin_Email'] = re.search(r'Admin Email: (.*)', cont).group(1)
                if '[' in data['Admin_Email']:
                    data['Admin_Email'] = data['Admin_Email'][:-9:]
            except:
                data['Admin_Email'] = '无记录'        
                  
            #self.driver.get(self.url)
            return data
        else:
            count = 0
            while not re.match('Domain Name:',cont):
                self.driver.refresh()
                sleep(5)
                try:
                    cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[8]/p").text
                except:
                    try:
                        cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[9]/p").text
                    except:
                        try:
                            cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[10]/p").text
                        except:
                            try:
                                cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[11]/p").text
                            except:
                                try:
                                    cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[12]/p").text
                                except:
                                    cont = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/ul/li[13]/p").text
                count = count + 1
                if count>=2:
                    break
            if re.match('Domain Name:',cont):
                try:
                    data['Registrant_phone'] = re.search(r'Registrant Phone: +(.*)', cont).group(1)
                except:
                    data['Registrant_phone'] = '无记录'
                try:
                    data['Registrant_Email'] = re.search(r'Registrant Email: (.*)', cont).group(1)
                    if '[' in data['Registrant_Email']:
                        data['Registrant_Email'] = data['Registrant_Email'][:-9:]
                except:
                    data['Registrant_Email'] = '无记录' 
                try:
                    data['Admin_phone'] = re.search(r'Admin Phone: +(.*)', cont).group(1)
                except:
                    data['Admin_phone'] = '无记录'        
                try:
                    data['Admin_Email'] = re.search(r'Admin Email: (.*)', cont).group(1)
                    if '[' in data['Admin_Email']:
                        data['Admin_Email'] = data['Admin_Email'][:-9:]
                except:
                    data['Admin_Email'] = '无记录' 
                #self.driver.get(self.url)
                return data
            else:
                data['Registrant_phone'] = '无记录'
                data['Registrant_Email'] = '无记录'
                data['Admin_phone'] = '无记录'
                data['Admin_Email'] = '无记录'
                #self.driver.get(self.url)
                return data


#print (cont)
   

#driver.back()

#driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/form/input[2]").click()


#input_.submit()







