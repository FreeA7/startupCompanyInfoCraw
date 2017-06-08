# -*- coding: UTF-8 -*-

import url_manager
import html_downloader
import html_parser
import html_outputer
import qixin_parser
import whois_parser
import urllib.parse
from bs4 import BeautifulSoup

class SpiderMain(object):    #可使用url管理器，下载器，解析器，输出器来完成功能
    
    def __init__(self):   #构造函数进行初始化
        self.fir_urls = url_manager.UrlManager()  #url管理器
        self.downloader = html_downloader.HtmlDownloader()  #下载器
        self.parser = html_parser.HtmlParser()  #解析器
        self.outputer = html_outputer.HtmlOutput()  #输出器
        self.qixin_parser = qixin_parser.QinxinParser()
        self.whois_parser = whois_parser.WhoisParser()


    #def craw(self,root_url):
	#	count = 1
	#	self.urls.add_new_url(root_url)  #将入口url放入urls队列中
	#	while self.urls.has_new_url():  #循环执行，只要urls队列中还有urls 
	#		try:
	#			new_url = self.urls.get_new_url()  #获取队列中还有的新url
	#			print 'craw %d : %s' % (count , new_url)
	#			html_cont = self.downloader.downloader(new_url) #使用下载器下载url 
	#			new_urls, new_data = self.parser.parse(new_url, html_cont)  #使用解析器解析网页内容返回新的url和内容
	#			self.urls.add_new_urls(new_urls)  #将解析器获取的新的url放入urls队列
	#			self.outputer.collect_data(new_data) #使用输出器收集数据
	#				if count == 1000:
	#				break
	#				count = count + 1
	#		except:
	#			print 'craw failed'
	#
	#		self.outputer.output_html()



    def craw(self,root_url):
        data_count = 0
        fir_url_count = 889
        self.fir_urls.add_new_url(root_url)
        while self.fir_urls.has_new_url():
            try:
                new_fir_url = self.fir_urls.get_new_url()   #从首页列表中取出新的未被处理的首页
                html_fir_cont = self.downloader.download(new_fir_url)         #下载新的首页
                new_tran_urls = self.parser.fir_tran_parse(new_fir_url,html_fir_cont)	#解析新首页提取所有中转网页
                
                #while new_tran_urls == None:
                #    html_fir_cont = self.downloader.download(new_fir_url)         #下载新的首页
                #    new_tran_urls = self.parser.fir_tran_parse(new_fir_url,html_fir_cont)	#解析新首页提取所有中转网页

                #for new_tran_url in new_tran_urls:
                #    if new_tran_url == None:
                #        html_fir_cont = self.downloader.download(new_fir_url)         #下载新的首页
                #        new_tran_urls = self.parser.fir_tran_parse(new_fir_url,html_fir_cont)	#解析新首页提取所有中转网页


                
                
                fir_list_count = 0
                #print (new_tran_urls)
                soup = BeautifulSoup(html_fir_cont,'html.parser',from_encoding = 'UTF-8')
                nodes = soup.find_all('ul',class_ = "list-main-eventset")
                nodes = nodes[1].find_all('li')
                for new_tran_url in new_tran_urls:                       #循环处理每个首页的内容
                        try:
                            
                        
                            if new_tran_url == 'https://www.itjuzi.com/investevents/foreign':
                                    continue

                            print ('Begin to craw tran_url '+ new_tran_url)
                            
                            html_tran_cont = self.downloader.download(new_tran_url)       #下载中转页

                            if html_tran_cont == '404':
                                print ('\tOpen tran_url '+ new_tran_url+' failed for 404')
                                continue
                            
                            new_fin_url = self.parser.tran_fin_parse(new_tran_url,html_tran_cont)          #提取目标页url

                            print ('\tBegin to craw '+ new_fin_url)
                            
                            #print (new_fin_url)
                            
                            html_fin_cont = self.downloader.download(new_fin_url)             #下载目标页

                            if html_fin_cont == '404':
                                print ('\tOpen fin_cont '+ new_fin_url+' failed for 404')
                                continue
                                        
                            new_data = self.parser.parse_fin(new_fin_url,html_fin_cont)     #解析目标页面上的数据

                            print ('\t'+new_fin_url+'itjuzi get it!')

                            #print (nodes[fir_list_count].find('i',class_ = "cell round").find('span'))
                            
                            new_data['TimeRound'] = nodes[fir_list_count].find('i',class_ = "cell round").find('span').get_text()
                            fir_list_count = fir_list_count + 1
                                    
                                        


                                #if new_data['key']==33518:
                                    #break

                            data_count = data_count + 1 			#已抓取网页计数
                                        
                            
                                    
                            new_data = self.qixin_parser.parse_qixin(new_data)

                            print ('\t'+new_fin_url+'qixinbao get it!')

                            new_data = self.whois_parser.parse_whois(new_data)
                            
                            print ('\t'+new_fin_url+'whois get it!')
                            
                            self.outputer.collect_data(new_data,html_fin_cont)		#数据收集
                            

                            print ('craw %d : %s complete!' % (data_count , new_fin_url))

                        #print (new_data)
                        
                        except:
                            print ('craw failed:' + new_fin_url)
                #if new_data['key']==33518:
                            #break
                fir_url_count = fir_url_count + 1 			#首页计数
                #if fir_url_count >= 8:
                    #break
                fir_url_str = str(fir_url_count)
                new_fir_url = "https://www.itjuzi.com/investevents?page=" + fir_url_str
                self.fir_urls.add_new_url(new_fir_url)        #放入下一个首页
            except:
                fir_url_count = fir_url_count + 1  # 首页计数
                #if fir_url_count >= 2:
                    #break
                fir_url_str = str(fir_url_count)
                new_fir_url = "https://www.itjuzi.com/investevents?page=" + fir_url_str
                self.fir_urls.add_new_url(new_fir_url)  # 放入下一个首页
        self.outputer.close()


if __name__=="__main__":    #main函数
    #root_url = "https://www.itjuzi.com/investevents"  #入口url
    root_url = "https://www.itjuzi.com/investevents?page=889"
    obj_spider = SpiderMain()  #创建一个spider
    obj_spider.craw(root_url)  #调用spider的craw方法来启动爬虫
