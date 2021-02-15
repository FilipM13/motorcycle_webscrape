from bs4 import BeautifulSoup as bs
import requests as rq

def ask(question: str, answers=[], q_type='closed'):
  '''
  question validation
  q_type: str - 'closed' (requires answers list), 'int', 'open'
  answers: list of str - list of possible answers, all lower case
  question: str - question you want to ask
  return:
  validated answer: str
  '''
  while True:
    #closed question
    if q_type == 'closed':
      pos = '/'.join(answers)
      response = input(f'{question} ({pos}) ').lower().replace(' ', '_')
      if response in answers:
        return response
      else:
        print('Invalid answer.')
    #numeric question
    elif q_type == 'int':
      response = input(f'{question} ').replace(' ', '')
      if response.isnumeric():
        response = abs(int(response))
        return response
      else:
        print('Invalid answer.')
    #open question
    elif q_type == 'open':
      response = input(f'{question} ').lower().replace(' ', '-')
      return response

def search(item_name, min_cc, max_cc, max_num=10):  
  #take page as html
  offers = []
  querry = (f'https://www.olx.pl/motoryzacja/motocykle-skutery/q-{item_name}'+
    f'/?search%5Bfilter_float_enginesize%3Afrom%5D={min_cc}'+
    f'&search%5Bfilter_float_enginesize%3Ato%5D={max_cc}'+
    f'&search%5Bfilter_enum_condition%5D%5B0%5D=notdamaged')
  html = rq.get(querry).text
  offers.append(f'--->\t{item_name}\t<---')
  print(f'--->\t{item_name}\t<---')
  soup = bs(html, 'lxml') #bs object
  offer_tags = soup.find_all('div', class_='offer-wrapper') #find specified thing : list
  #check numbers of offer
  if len(offer_tags) <= max_num:
    max_num == len(offer_tags) - 1
  #find name, price and link for every offer
  for i in offer_tags[0:max_num+1]:
    target = i.find('h3', class_="lheight22 margintop5")
    link = target.find('a')['href']
    name = target.find('a').text
    price = i.find('p', class_='price').text
    offers.append(f'{name} - {price} -> {link}'.replace('\n', ' '))
    print(f'{name} - {price}'.replace('\n', ' '))
  #return offers as list
  return offers

def save(offers: list, file_name: str):
  #save offers to text file
  file = open(f'{file_name}.txt', 'w')
  file.write('\n'.join(offers))
  print('File saved in directory of app.')

do = True
while do == True:
  what = ask('What motorcycle do you want to find?', q_type='open')
  cc_min = ask('Enter minimal CC:', q_type='int')
  cc_max = ask('Enter maximal CC:', q_type='int')
  num = ask('How many offers do you want to get?', q_type='int')
  #searching
  offs = search(what, cc_min, cc_max, num)
  #save offers or not?
  valid = False
  remember = ask('Do you want to save offers (links included)?', answers=['yes', 'no'], q_type='closed')
  #saving offers
  if remember == 'yes':
    name = ask('Enter file name:', q_type='open')
    save(offs, name)
  #exit or not?
  cont = ask('Do you want to find another motorcycle?', ['yes', 'no'], q_type='closed')
  if cont == 'no':
    do = False
