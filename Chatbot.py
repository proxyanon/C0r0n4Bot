import requests

response = requests.get('https://coronavirus-19-api.herokuapp.com/countries/brazil')

dic = eval(str(response.json()))

class Chatbot():

    def __init__(self, name):
        self.name = name

    def send(self, text):
        if text.upper() == 'CASOS':
            return dic['cases']
        if text.upper() == 'MORTES':
            return dic['deaths']
        if text.upper() == 'CURADOS':
            return dic['recovered']
        if text.upper() == 'CRITICOS':
            return dic['critical']


