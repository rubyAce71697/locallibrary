from bs4 import BeautifulSoup
import requests
import csv

web = requests.get('http://www.odysseypublications.com/publicationsISBNIndex.php')
print web
#print web.content
soup = BeautifulSoup(web.content)
print soup.title

div = soup.findAll('p',{'class': 'MainLHS'})
#SSprint div
#table = div.find_next('table')
tr = soup.findAll('tr',{'style':"background-color: #e6e6e6"})
for i in tr:
    tds = i.findAll('td',{'class': 'MainLHSP'})
    print
    for itd in tds:
        #print "--"*40
        a = itd.find('a',{'class': 'MainLHSP'})
        url =  a['href'].replace("\r\r\n","").replace('\r\n',"") if a else "",
        url =  url[0]
        #print url
        if a:
            data = requests.get(url)
            h_soup = BeautifulSoup(data.content)
            table =  h_soup.find('table',{'style':"width: 728px; height: 450px; margin: 0px auto; padding: 0px; border-width: 0px; background-color: #ffffff"})
            td = table.find('td',{'style':"width: 413px; background-color: #f6f6f6"})
            #print repr(td)
            desc = td.find('p',{'class':"MainLHS"})
            #print desc.text.strip()
            td_author = table.find('td',{'style':"width: 314px"})
            #print td_author
            #print td_author.findAll('a', {'class':'MainRHS'})
            """
            authors_list =  [ i.text for i in td_author.findAll('a', {'class':'MainRHS'}) if ".com" not in i]
            print authors_list
            
            with open("authors_scrapped.csv", "a") as csvfile:
                spamwriter = csv.writer(csvfile)
                for i in authors_list:
                    if len(i.split()) == 2:
                        spamwriter.writerow([i.split()[1],i.split()[0]])
                

            """


            tr_isbn = table.findAll('tr')
            #print len(tr_isbn)
            print "**"*40
            for i in tr_isbn:
                td = i.findAll('td')
                print " ".join([k.text.strip().replace("\n","").replace("\r","").replace("\t","") for k in td])
                #print
            
            
        print itd.text.strip() + " ",
        break


        