from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://timesofindia.indiatimes.com/').text
soup = BeautifulSoup(html_text, "lxml")
sub = soup.find_all("ul", class_= "list8" or "list9" or "list2")
for links in sub:
    for link in links.find_all("li"):
        site_link = link.a["href"]
        full_link = f"https://timesofindia.indiatimes.com/{site_link}"
        another_html_req = requests.get(f'{full_link}').text
        another_soup = BeautifulSoup(another_html_req, "lxml")
        
        for content in another_soup.find_all("div", class_="_3lvqr clearfix"):
            title = content.find("div", class_="_2NFXP").h1.text
            para_content = content.find("div", class_="ga-headlines").text.split(".")
            date_and_time = content.find("div", class_="_3Mkg- byline").text.split("|")
            if len(date_and_time) == 1:
                date_and_time = content.find("div", class_="_3Mkg- byline").text
            else:
                date_and_time = date_and_time[len(date_and_time)-1]
            dnt = date_and_time.split(":")
            if(dnt[0] =="Updated" ):
                date_and_time = dnt[1] + dnt[2]
            edited_para_content = '\n'.join(para_content)
            edited_para_content = edited_para_content.replace("â","'")
            with open("home.txt", "a") as file:
                file.write(f"\nTITLE:\n{title}\n\nLINK:\n{full_link}\n\nDATE_&_TIME:\n{date_and_time}\n\nTEXT:\n{title}\n{edited_para_content}\n\n")