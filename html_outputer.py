# -*- coding: UTF-8 -*-   

class HtmlOutput(object):
	
    def __init__(self):
        self.f = open('outputTest35.txt','w')
        self.f.write("项目key值\t")
        self.f.write("橘子时间\t")
        self.f.write("项目名称\t行业标签\t细分标签\t地址\t项目网址")
        self.f.write("\t公司类型\t法定代表人\t成立日期\t工商企业地址\t经营范围\t联系电话\tEmail")
        self.f.write("\tRegistrant Phone")
        self.f.write("\tRegistrant Email")
        self.f.write("\tAdmin Phone")
        self.f.write("\tAdmin Email")
        for i in range(10):
            self.f.write("\t橘子标签"+str(i+1))
        self.f.write("\t公司名称\t成立时间\t运营状态")
        self.f.write("\t是否急需融资")
        self.f.write("\t融资记录\t融资次数")
        for i in range(4):
            self.f.write("\t融资时间"+str(i+1))
            self.f.write("\t融资轮次"+str(i+1))
            self.f.write("\t融资额度"+str(i+1))
            for j in range(4):
                self.f.write("\t投资人"+str(i+1)+','+str(j+1))
        self.f.write('\t项目团队')
        for i in range(3):
            self.f.write("\t姓名"+str(i+1))
            self.f.write("\t职位"+str(i+1))
            self.f.write("\t简介"+str(i+1))
        self.f.write("\t项目简介\n")
        self.f.flush()
    

    def collect_data(self,data,html):
        if data is None:
            return
        self.f.write(data['key']+'\t')
        self.f.write(data['TimeRound']+'\t')
        self.f.write(data['Project_name']+'\t')
        self.f.write(data['Industry_tag']+'\t')
        self.f.write(data['Segmentation_tags']+'\t')
        self.f.write(data['Address']+'\t')
        self.f.write(data['Project_site']+'\t')

        self.f.write(data['Company_type']+'\t')
        self.f.write(data['Legal_representative']+'\t')
        self.f.write(data['Establishment_data']+'\t')
        self.f.write(data['TIB_adress']+'\t')
        self.f.write(data['Business_scope']+'\t')
        self.f.write(data['Contact_phone']+'\t')
        self.f.write(data['E-mail']+'\t')

        self.f.write(data['Registrant_phone']+'\t')
        self.f.write(data['Registrant_Email']+'\t')
        self.f.write(data['Admin_phone']+'\t')
        self.f.write(data['Admin_phone']+'\t')
        
        for i in range(10):
            self.f.write(data['Juzi_tag'+str(i+1)]+'\t')
        self.f.write(data['Company_name']+'\t')
        self.f.write(data['Setup_time']+'\t')
        self.f.write(data['Operating_conditions']+'\t')
        self.f.write(data['Financing_needs']+'\t')
        self.f.write(data['Financing_records']+'\t')
        self.f.write(str(data['Financing_number'])+'\t')
        for i in range(4):
            self.f.write(data['Financing_time'+str(i+1)]+'\t')
            self.f.write(data['Financing_rounds'+str(i+1)]+'\t')
            self.f.write(data['Financing_limit'+str(i+1)]+'\t')
            for j in range(4):
                self.f.write(data['Investors'+str(i+1)+','+str(j+1)]+'\t')
        self.f.write(data['Project_team'])
        for i in range(3):
            self.f.write(data['Team_name'+str(i+1)]+'\t')
            self.f.write(data['Team_position'+str(i+1)]+'\t')
            self.f.write(data['Team_introduction'+str(i+1)]+'\t')
        self.f.write(data['Introduction'])
        self.f.write('\n')
        self.f.flush()

        file = open(data['key']+'html.txt','wb')
        file.write(html)
        file.close()
        

    def close(self):
        self.f.close()
                

