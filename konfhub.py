# requests module allows you to send HTTP requests
import requests
# urllib module allows you to get data from url
from urllib.request import urlopen

def all_contents():

	url="https://o136z8hk40.execute-api.us-east-1.amazonaws.com/dev/get-list-of-conferences"

	response=requests.get(url)

	a=response.json()

	months={
		'jan':'January',
		'feb':'February',
		'mar':'March',
		'apr':'April',
		'may':'May',
		'jun':'June',
		'jul':'July',
		'aug':'August',
		'sep':'September',
		'oct':'October',
		'nov':'November',
		'dec':'December'
	}

	events=a['paid']+a['free']

	contents=[]

	for i in events:
		
		date=i['confStartDate'][:2]
		date=int(date)

		if date not in (11,12,13):
			if date%10==1:
				date=str(date)+'st'
			elif date%10==2:
				date=str(date)+'nd'
			elif date%10==3:
				date=str(date)+'rd'
			else:
				date=str(date)+'th'
		else:
			date=str(date)+'th'

		month=months[i['confStartDate'][3:6].lower()]
		year=i['confStartDate'].split(',')[1]
		contents.append(i['confName']+', '+month+' '+date+','+year+', '+i['city']+', '+i['state']+', '+i['country']+', '+i['entryType']+'. '+i['confUrl'])
	return contents

def print_all_contents():
	data=all_contents()
	print('--------------------')
	print('Contents in a human readable')
	print('--------------------')

	for count,i in enumerate(data,1):
		print(str(count)+'. '+i)

def print_all_exact():
	data=all_contents()
	exact=[]
	
	for i in range(len(data)):
		if data[i] in data[i+1:]:
			exact.append(data[i])
	
	print('--------------------')
	print('Exact duplicates')
	print('--------------------')
	
	for count,i in enumerate(exact,1):
		print(str(count)+'. '+i)

def remove_common_words(data,words):
	new_data=[]
	
	for j in data:
		if j.lower() not in words:
			new_data.append(j)
	return new_data


def print_all_semantic():
	data=all_contents()
	semantic=[]
	black=[]
	url=urlopen('https://raw.githubusercontent.com/deepaksaini14896/100_common_words/main/100_common_words.txt')
	words=[]
	
	for i in url.readlines():
		words.append(i.decode('utf-8').rstrip())
	
	for i in range(len(data)):
		index=[]
		if i not in black:
			for j in range(i+1,len(data)):
				if j not in black:
					for k in remove_common_words(data[i].split(',')[0].split(),words):
						if k in data[j].split(',')[0].split():
							if len(index)==0:
								index.append(i)
							index.append(j)
							black.append(j)
							break
		if len(index)>=1:
			semantic.append(index)
	
	print('--------------------')
	print('Semantic duplicates')
	print('--------------------')
	
	for i in semantic:
		for count,j in enumerate(i,1):
			print(str(count)+'. '+data[j])
		print('\n')
		print('-------------------------------------------')
		print('\n')


task=int(input('1: Contents in a human readable \n2: Exact duplicates \n3: Semantic duplicates \n4: Exit \nPlease select number: '))
if task==1:
	print_all_contents()
elif task==2:
	print_all_exact()
elif task==3:
	print_all_semantic()
elif task==4:
	print('--------------------')
	print('Exit')
	print('--------------------')
	pass
else:
	print('--------------------')
	print('Wrong number')
	print('--------------------')