import re
import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd

search='causal'

url = 'https://nips.cc/virtual/2024/papers.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# get all accepted papers
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser').body.main

pattern = re.compile(r"^/virtual/2024/poster/.*")
all_accepted_papers = soup.find_all('a', href=pattern)

# save all accepted papers to excel (sheet[0])
workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet("all")
for i in range(len(all_accepted_papers)):
    worksheet.write(i, 0, all_accepted_papers[i].text)
workbook.save("NeurIPS2024_accepted_papers.xls")

# search for papers with {search} in the title
data = xlrd.open_workbook('NeurIPS2024_accepted_papers.xls')
table = data.sheets()[0]
all_papers = table.col_values(colx=0)
selected_papers=[]
for i in range(len(all_papers)):
    if search in all_papers[i].lower():
        selected_papers.append(all_papers[i])

# save the found papers to excel (sheet[1])
worksheet = workbook.add_sheet(search)
for i in range(len(selected_papers)):
    worksheet.write(i, 0, selected_papers[i])
workbook.save("NeurIPS2024_accepted_papers.xls")
