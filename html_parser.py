# -*- coding: UTF-8 -*-   

from bs4 import BeautifulSoup
import re
import urllib.parse

class HtmlParser(object):

    def _get_fir_urls(self,page_url,soup):
        new_urls = set()
        #中转页：https://www.itjuzi.com/investevents/15746    （1~无穷）（数字是结尾，去掉重复的）
        links = soup.find_all('a',href = re.compile(r"https://www\.itjuzi\.com/investevents/\d*"))
        for link in links:
            new_urls.add(link['href'])
        return new_urls

    def _get_tran_urls(self,page_url,soup):
        #<div class="block-inc-fina"><table><tbody><tr>
        link = soup.find('div',class_="block-inc-fina").find('a',class_="name")
        return link['href']
    

    def _get_fin_data(self,page_url,soup):
        
        new_data = {}
        fin_null = "无记录"
        formart = '0123456789'
        q=''
        for c in page_url:
            if c in formart:
                q = q + c

        new_data['key'] = q
        p_p = re.compile('\s+')

        #if soup.find('svg',id = submarine_container

        
        Project_name = soup.find('div',class_="picinfo").find('div',class_="line-title").find('span',class_="title").find('b').get_text().lstrip()
        num = Project_name.index('(')
        Project_name = Project_name[0:num]
        #Project_name = Project_name[:20].rstrip()
        Project_name = re.sub(p_p,'',Project_name)
        new_data['Project_name'] = Project_name
        new_data['Industry_tag'] = soup.find('span',class_="scope c-gray-aset").find('a').get_text()
        new_data['Segmentation_tags'] = soup.find('span',class_="scope c-gray-aset").find('a',href = re.compile(r"http://www\.itjuzi\.com/company\?scope=\d*&sub_scope=\d*")).get_text()
        adress =  soup.find('span',class_="loca c-gray-aset").find_all('a')
        new_data['Address'] = adress[0].get_text()+adress[1].get_text()
        if new_data['Address']=='':
            new_data['Address'] = '无记录'
        new_data['Project_site'] = soup.find('a',class_="weblink").get_text()
        if new_data['Project_site']=='':
            new_data['Project_site'] = '无记录'

        
        intr = soup.find('div',class_="des").get_text().strip()
        intr = re.sub(p_p,'',intr)
        
        new_data['Introduction'] = intr
        
        inf = soup.find('div',class_="des-more").find_all('div')
        inf[0] = inf[0].find('span').get_text()
        inf[1] = inf[1].find('span').get_text()
        new_data['Company_name'] = inf[0][5:]
        new_data['Setup_time'] = inf[1][5:]
        new_data['Operating_conditions'] = inf[2].find('span').get_text()


        
        juzi_tags = soup.find('div',class_ = "tagset dbi c-gray-aset").find_all('span')
        for i in range(10):
            try:
                new_data['Juzi_tag'+ str(i+1)] = juzi_tags[i].get_text()
            except:
                new_data['Juzi_tag'+ str(i+1)] = fin_null

        
       # for juzi_tag in juzi_tag:
       #     juzi_tag_count = juzi_tag_count + 1
       #     new_data['Juzi_tag'+ str(juzi_tag_count)] = juzi_tag.get_text()


            
        if soup.find('span',class_ = "tag bg-c"):
            new_data['Financing_needs'] = "急需融资"
        else:
            new_data['Financing_needs'] = "不急需融资"
        if soup.find('table',class_="list-round-v2"):
            new_data['Financing_records'] = "有融资记录"
            fin_nodes = []
            fin_nodes=soup.find('table',class_="list-round-v2").find_all('tr')
            
            fin_count = 0
            for fin_node in fin_nodes:
                fin_count = fin_count + 1
            new_data['Financing_number'] = fin_count
            
            
            for i in range(4):
                try:
                    fin_nodes[i] = fin_nodes[i].find_all('td')
                    new_data['Financing_time'+str(i+1)] = fin_nodes[i][0].find('span',class_="date c-gray").get_text()
                    new_data['Financing_rounds'+str(i+1)] = fin_nodes[i][0].find('span',class_="mobile-block").find('span').find('a').get_text()
                    new_data['Financing_limit'+str(i+1)] = fin_nodes[i][2].find('span').find('a').get_text()
                    fin_inv_node = []
                    for fin_a_node in fin_nodes[i][3].find_all('a'):
                        fin_inv_node.append(fin_a_node)
                    for fin_a_node in fin_nodes[i][3].find_all('span'):
                        fin_inv_node.append(fin_a_node)

                    
                    for j in range(4):
                        try:
                            new_data['Investors'+str(i+1)+','+str(j+1)] = fin_inv_node[j].get_text()
                        except:
                            new_data['Investors'+str(i+1)+','+str(j+1)] = fin_null
                        
                except:
                    new_data['Financing_time'+str(i+1)] = fin_null
                    new_data['Financing_rounds'+str(i+1)] = fin_null
                    new_data['Financing_limit'+str(i+1)] = fin_null
                    for j in range(4):
                        new_data['Investors'+str(i+1)+','+str(j+1)] = fin_null
            


            
          #  if fin_count == 0:
          #      for i in range(3):
          #          new_data['Financing_time'+str(i+1)] = fin_null
          #          new_data['Financing_rounds'+str(i+1)] = fin_null
          #          new_data['Financing_limit'+str(i+1)] = fin_null
          #  elif fin_count == 1:
          #      fin_nodes[0] = fin_nodes[0].find('td')
          #      new_data['Financing_time'+str(1)] = fin_nodes[0][0].find('span',class_="date c-gray").get_text()
          #      new_data['Financing_rounds'+str(1)] = fin_nodes[0][0].find('span',class_="mobile-block").find('span').find('a').get_text()
          #      new_data['Financing_limit'+str(1)] = fin_nodes[0][2].find('span').find('a').get_text()

            
          #  for i in range(3):
          #      fin_nodes[i] = fin_nodes[i].find_all('td')
          #      new_data['Financing_time'+str(i)] = fin_nodes[i][0].find('span',class_="date c-gray").get_text()
          #      new_data['Financing_rounds'+str(i)] = fin_nodes[i][0].find('span',class_="mobile-block").find('span').find('a').get_text()
          #      new_data['Financing_limit'+str(i)] = fin_nodes[i][2].find('span').find('a').get_text()
          #      fin_inv_node = []
          #      for fin_a_node in fin_node[3].find_all('a'):
          #          fin_inv_node.append(fin_a_node)
          #      for fin_a_node in fin_node[3].find_all('span'):
          #          fin_inv_node.append(fin_a_node)
          #      for i in range(4):
          #          if fin_inv_node[i]:
          #              new_data['Investors'+str(i)+','+str(i)]='无'
          #          else:
          #              new_data['Investors'+str(i)+','+str(i)]=fin_inv_node[i].get_text()
            
            
        else:
            new_data['Financing_records'] = "没有融资记录"
            new_data['Financing_number'] = 0
            for i in range(4):
                new_data['Financing_time'+str(i+1)] = fin_null
                new_data['Financing_rounds'+str(i+1)] = fin_null
                new_data['Financing_limit'+str(i+1)] = fin_null
                for j in range(4):
                    new_data['Investors'+str(i+1)+','+str(j+1)] = fin_null
            


            
        if soup.find('ul',class_="list-prodcase limited-itemnum"):
            new_data['Project_team'] = "有项目团队信息"
            team_infs = []
            team_infs = soup.find('ul',class_="list-prodcase limited-itemnum").find_all('li')
            p_p_p = re.compile('\s+')
            for i in range(3):
                try:
                    new_data['Team_name'+str(i+1)] = team_infs[i].find('span',class_="c").get_text()
                    new_data['Team_position'+str(i+1)] = team_infs[i].find('span',class_="c-gray").get_text()
                    team_intr = team_infs[i].find('p').get_text().strip()
                    team_intr = re.sub(p_p_p,'',team_intr)
                    new_data['Team_introduction'+str(i+1)] = team_intr
                except:
                    new_data['Team_name'+str(i+1)] = fin_null
                    new_data['Team_position'+str(i+1)] = fin_null
                    new_data['Team_introduction'+str(i+1)] = fin_null
            

                
        #    for team_inf in team_infs:
        #        new_data['Team_name'+str(team_count)] = team_inf.find('span',class_="c").get_text()
        #        new_data['Team_position'+str(team_count)] = team_inf.find('span',class_="c-gray").get_text()
        #        new_data['Team_introduction'+str(team_count)] = team_inf.find('p').get_text().strip()
        else:
            new_data['Project_team'] = "没有项目团队信息"
            for i in range(3):
                new_data['Team_name'+str(i+1)] = fin_null
                new_data['Team_position'+str(i+1)] = fin_null
                new_data['Team_introduction'+str(i+1)] = fin_null
        return new_data
			
		

    def fir_tran_parse(self,page_url,html_cont):
        if page_url is 	None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding = 'UTF-8')
        new_urls = self._get_fir_urls(page_url,soup)
        return new_urls

    def tran_fin_parse(self,page_url,html_cont):
        if page_url is 	None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding = 'UTF-8')
        new_url = self._get_tran_urls(page_url,soup)
        return new_url

    def parse_fin(self,page_url,html_cont):
        if page_url is 	None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding = 'UTF-8')
        new_data = self._get_fin_data(page_url,soup)
        return new_data
    
    def parse_fir(self,html_cont,count):
        print (html_cont[:10:])
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding = 'UTF-8')
        nodes = soup.find_all('ul',class_ = "list-main-eventset")
        nodes = nodes[1].find_all('li')
        time_round = nodes[count].find('i',class_ = "cell round").find('span').get_text()
        return str(time_round)







#	def _get_new_urls(self,page_url,soup):
#		new_urls = set()
#		links = soup.find_all('a',href = re.compile(r"/view/\d+\.htm"))
#		for link in links:
#			new_url = link['href']
#			new_full_url = urlparse.urljoin(pagr_url,new_url)
#			new_urls.add(new_full_url)
#		return new_urls
#
#	
#	def _get_new_data(self,page_url,soup):
#		res_data = {}
#		title_node = sou.find('div',class_ = "lemmaWgt-lemmaTitle-title").find("h1")
#		res_data['title'] = title_node.get_text()
#
#		summary_node = soup.find('div',class_ = "lemma-summary")
#		res_data['summary'] = summary_node.get_text()
#		return res_data
#
#
#	def parse(self,page_url,html_cont):
#		if page_url is 	None or html_cont is None:
#			return
#		soup = BeautifulSoup(html_cont,'html.parser',from_encoding = 'UTF-8')
#		new_urls = self._get_new_urls(page_url,soup)
#		new_data = self._get_new_data(page_url,soup)
#		return new_urls,new_data
