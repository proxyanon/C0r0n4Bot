import requests

response = requests.get('https://coronavirus-19-api.herokuapp.com/countries/brazil')

dic = eval(str(response.json()))

class Chatbot():

    def __init__(self, name):
        self.name = name

    def send(self, text):
        #if msg == 'help':
            
        if text == 'cases':
            return dic['cases']
        #if msg == 'deaths':


