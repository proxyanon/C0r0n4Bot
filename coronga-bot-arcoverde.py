from requests import get
from datetime import date
from os import path, walk, makedirs as mkdir, remove, getcwd
from time import sleep, strftime as time
from sys import argv
from bs4 import BeautifulSoup as bs4
from urllib.parse import unquote_plus as urldecode
import twitter

config={
	'cache_path' : 'cache',
	'delay' : 60,
	'beep' : False,
	'beep_times' : 1,
	'headers' : {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'},
	'api' : {
		'consumer_key' : 'wDwm9DsDa4mNHF4G2BuMno6Ju',
		'consumer_secret' : 'L4CnnCuuQRC2wSHRK6OtPjQtCO8AJCx3MIRRFc1yMty0XjSoq4',
		'access_token_key' : '818269355771383808-nEntBS1Yxe3qHp6hGDoqeSGf2xJXwbI',
		'access_token_secret' : 'kumwpq3LoPdBvgAUTxf9aTE2G69HZY21xI7L6dE5eMFAY'
	},
	'message' : ''
}

dev=False
arguments=['-f','--force','-d','--dev','-b','--beep']

for arg in argv:

	arg = arg.strip().lower()

	if arg in arguments:
		
		if arg in ['-f','--force']:
			
			try:
				for val in argv:
					if val!=argv[0] and val not in arguments:
						config['delay'] = int(val)
			except:
				print('[x] Delay invÃ¡lido !')
				exit()

		if arg in ['-d','--dev']:
			
			print('[+] DEVMODE ON!')
			dev=True

		if arg in ['-b','--beep']:
			
			config['beep']=True
			
			try:
				config['beep_times']=int(argv[argv.index(arg)+1])
			except:
				print('[X] Beep times invÃ¡lido, prosseguindo com 1')
				config['beep_times']=1
	
	elif arg!=argv[0]:
		
		try:
		
			config['delay'] = int(arg)

			if config['delay']<60 and '--force' not in argv and '-f' not in argv:
				print('[x] Tempo minÃ­mo de 1 minuto')
				config['delay']=60
		
		except:
			print('[x] Delay invÃ¡lido !')
			exit()


if path.exists(config['cache_path'])==False:
	mkdir(config['cache_path'])

def beep(beep_times=1):
	for i in range(beep_times):
		print("\a")
		sleep(1)

def cache_image(src_url,dst_path,headers=config['headers']):
	
	r=get(src_url,headers=headers)
	img_content=r.content

	#print(img_content)

	handle=open(dst_path,'wb')
	handle.write(img_content)
	handle.close()

def check_cache(image_name):
	return path.exists(path.join(config['cache_path'],image_name))

def clean_cache():
	for paths,dirs,files in walk(config['cache_path']):
		for file in files:
			remove(path.join(paths,file))

def tweet(api,image,message):
	api.PostUpdate(status=message,media=image)

def get_content(request_url,headers=config['headers']):
	return get(request_url,headers=headers).content

def get_month_by_number(number):
	return ['Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][number+1]

def get_month_by_name(name,str_mode=False):
	
	ret=int([month.lower() for month in ['Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']].index(name.lower()))+1

	if str_mode:

		ret='{0}'.format(ret)

		if int(ret)<10:
			ret='0{0}'.format(ret)

	return ret

api=twitter.Api(
	consumer_key=config['api']['consumer_key'],
	consumer_secret=config['api']['consumer_secret'],
	access_token_key=config['api']['access_token_key'],
	access_token_secret=config['api']['access_token_secret']
)

try:
	
	while True:

		today=date.today()
		hours=time('%H:%M')

		request_url="http://www.arcoverde.pe.gov.br/busca.php?pagina=1&procurar=Boletim"
		soup=bs4(get_content(request_url),'html.parser')

		items=soup.find_all('div',class_="panel-body")

		item=''

		a=[a.get('href') for item in items for a in item.find_all('a',class_='legenda')]
		i=[i.get_text() for item in items for i in item.find_all('i')]

		index=0

		day_notice=i[index].split(' de ')[0]
		month_notice=get_month_by_name(i[index].split(' de ')[1],True)
		year_notice=i[index].split(' de ')[2]

		full_date_notice='{0}/{1}/{2}'.format(day_notice,month_notice,year_notice).strip().replace(' ','')
		full_date_today=today.strftime('%d/%m/%Y')

		if full_date_notice==full_date_today:

			notice_url=a[index]
			soup_notice=bs4(get_content(notice_url),'html.parser')

			img_src=soup_notice.find_all('div',class_='texto')[0].find_all('img')[0].get('src')
			img_link='http://www.arcoverde.pe.gov.br{0}'.format(img_src)
			
			image_name=urldecode(img_src.split('/')[len(img_src.split('/'))-1])
			image_name=image_name.replace('"','').replace('\\', '')

			if 'corona' in image_name.lower():

				if dev:
					dev='({0})'.format(image_name)
				else:
					dev=''

				if check_cache(image_name)==False:

					if config['beep']:
						beep(config['beep_times'])
					
					print('[+] UPDATE {0} - {1} {dev}'.format(full_date_today,hours,dev=dev))

					config['message']='\N{MICROBE} BOT Coronga update - {0}'.format(today.strftime('%d/%m/%Y'))

					clean_cache()
					cache_image(src_url=img_link,dst_path=path.join(config['cache_path'],image_name))
					tweet(api=api,image=path.join(getcwd(),config['cache_path'],image_name),message=config['message'])
				
				else:
					print('[-] Imagem no cache {dev}'.format(dev=dev))

		else:

			delay_min=round(config['delay']/60)
			delay_legend='minuto'

			if delay_min>1:
				
				delay_legend='minutos'
			
				if delay_min==60:
					delay_min=round(delay_min/60)
					delay_legend='hora'
				elif delay_min>60:
					delay_min=round(delay_min/60)
					delay_legend='horas'

			elif delay_min<1:

				delay_legend='segundo'

				if config['delay']>1:
					delay_legend='segundos'


			print('[-] Nada para atualizar, tentando novamente em {0} {1} {2} - {3}'.format(delay_min,delay_legend,full_date_today,hours))

		sleep(config['delay'])



except:
	pass
