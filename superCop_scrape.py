from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict

with open("results-encrypt.html") as wp:
	soup = BeautifulSoup(wp.read(),"html5lib")

with open("computers.html") as wp:
	comp_soup = BeautifulSoup(wp.read(),"html5lib")

computer_tables = soup.find_all("table", attrs={"bgcolor":"#dddddd"})
computer_tables.extend(soup.find_all("table", attrs={"bgcolor":"#bbbbbb"}))

comp_info = comp_soup.find_all("tr")

print("Soup is made")

all_systems = {}
comp_stats = {}

for computer in computer_tables:
	comp_name = computer.find('a').get('href')[14:-4].split('-')[-1]

	arch_info = None
	for tag in comp_info:
		des_tag = False
		for chil in tag.findChildren():
			if chil.string == comp_name:
				des_tag = True
		if des_tag:
			arch_info = tag.find_all('td')[2]
	print(arch_info, end='*************')
	try:
		direct_info = arch_info.string.split(";")[1].replace(" ","")
	except:
		#direct_info = arch_info.findChildren()[0].split(";")[1].replace(" ","")
		direct_info = next(arch_info.children).split(";")[1].replace(" ","")
	comp_stats[comp_name] = direct_info.rsplit('x',1)
	print(comp_stats[comp_name])

	for test_table in computer.find_all("table", attrs={'border':''}):
		if len(test_table) > 1:
			test = test_table.th.string
			for encrypt_system in test_table.find_all("tr", attrs={'align':'right'}):
				tds = encrypt_system.find_all("td")
				test_value = tds[0].string if len(tds) == 2 else tds[1].string
				test_value = test_value.split('?')[0]
				if all_systems.get(encrypt_system.tt.string):
					if all_systems[encrypt_system.tt.string].get(test):
						all_systems[encrypt_system.tt.string][test].append((comp_name,test_value))
					else:
						all_systems[encrypt_system.tt.string][test]=[(comp_name,test_value)]
				else:
					all_systems[encrypt_system.tt.string] = {test:[(comp_name,test_value)]}
for en_sys in all_systems:
	for test_dict in all_systems[en_sys]:
		all_systems[en_sys][test_dict].sort(key=lambda tup: tup[0])
	all_systems[en_sys] = OrderedDict(sorted(all_systems[en_sys].items()))
all_systems = OrderedDict(sorted(all_systems.items()))

print("Dictionary made, parsing html")

#htmlString = """<html>
#<head>
#<meta http-equiv="content-type" content="text/html; charset=utf-8">
#<title>
#Measurements of public-key cryptosystems, indexed by encryption system
#</title>
#</head>
#<body>\n"""
#
#for encrypt_system in all_systems:
	#htmlString += '<table width="100%" border="1">\n<tr><td align=middle colspan="18"><h1>{}</h1></td></tr>\n'.format(encrypt_system)
	#htmlString += '<tr>'
	#for test in all_systems[encrypt_system]:
		#htmlString+='<td align=middle colspan="2">{}</td>'.format(test)
	#htmlString += '</tr>\n'
	#for i in range(len(all_systems[encrypt_system]['Secret key'])):
		#htmlString += '<tr>'
		#for test in all_systems[encrypt_system]:
			#htmlString += '<td align=middle>{}</td><td align=middle">{}</td>'.format(all_systems[encrypt_system][test][i][0],all_systems[encrypt_system][test][i][1])
		#htmlString += '</tr>\n'
	#htmlString += '</table>\n'
#
#htmlString+='\n</body></html>'
#
#with open('results.html','w') as results_file:
	#results_file.write(htmlString)
csvString = ''

for encrypt_system in all_systems:
	csvString += '{}\nComputer, Cores, MHz per'.format(encrypt_system)
	for test in all_systems[encrypt_system]:
		csvString+=',{}'.format(test)
	csvString+='\n'
	for i in range(len(all_systems[encrypt_system]['Secret key'])):
		comp_name = all_systems[encrypt_system][test][i][0]
		csvString+= '{}'.format(comp_name)
		stats = comp_stats[comp_name]
		csvString+= ',{},{}'.format(stats[0],stats[1])
		for test in all_systems[encrypt_system]:
			csvString += ',{}'.format(all_systems[encrypt_system][test][i][1])
		csvString+='\n'

with open('results.csv','w') as results_file:
	results_file.write(csvString)
