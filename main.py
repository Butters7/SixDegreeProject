# Импортируем необходимые библиотеки
from typing import List
import networkx as nx
import requests

# Определяем класс для нелюдей
class Person:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, person):
        self.connections.append(person)
# Определяем класс приложения
class SixDegreesApp:
    def __init__(self):
        self.graph = nx.Graph()
        self.exceptions = 0
        self.connections = {}
        self.token = '08f8682608f8682608f86826850bec68c4008f808f868266ca567b35dc8f37858cb4172'
        self.version = 5.92


    # Метод для добавления человека в граф
    def add_person(self, name):
        person = Person(name)
        self.graph.add_node(person)

    # Метод для добавления связи между двумя людьми в граф
    def add_connection(self, name1, name2):
        person1 = self.get_person(name1)
        person2 = self.get_person(name2)
        person1.add_connection(person2)
        person2.add_connection(person1)
        self.graph.add_edge(person1, person2)

    # Метод для получения объекта человека по его имени
    def get_person(self, name):
        for node in self.graph.nodes():
            if node.name == name:
                return node
        return None
    
    def update_amount(self, id1, ids : List):
        if ids != 'private':
            self.add_person(id1)
            for id2 in ids:
                self.add_person(id2)
                self.add_connection(id1, id2)
                self.connections[f'{id1}<->{id2}'] = 1
            


    # def find_shortest_path(self, name1, name2):
    #     person1 = self.get_person(name1)
    #     person2 = self.get_person(name2)
    #     shortest_path = nx.shortest_path(self.graph, person1, person2)
    #     print(f"Кратчайший путь между {name1} и {name2}: {[node.name for node in shortest_path]}")
    #     print(nx.shortest_path_length(self.graph, person1, person2))

    # Метод для поиска кратчайшего пути между двумя людьми в графе
    def find_shortest_path(self, name1, name2):
        person1 = self.get_person(name1)
        person2 = self.get_person(name2)

        try:
            distance = nx.shortest_path_length(self.graph, person1, person2)
            if distance != 0:
                self.connections[f'{name1}<->{name2}'] = distance

        except nx.exception.NetworkXNoPath:
            self.exceptions += 1

        

    # Метод для запуска приложения
    def run(self, name1, name2):
        self.find_shortest_path(name1, name2)

    def create_response(self, first_id):
        return requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'access_token' : self.token,
                                    'v' : self.version,
                                    'user_id' : first_id
                                })
    
    def get_data_from_response(self, first_id):
        response = self.create_response(first_id)
        print(response)
        try:
            data = response.json()['response']['items']
            return data
        except:
            return 'private'


    # from vk
    def popopo(self, first_id):

        data = self.get_data_from_response(first_id)
        self.update_amount(first_id, data)

        for i in range(len(data) - 350):
            new_id = data[i]
            new_data = self.get_data_from_response(new_id)
            self.update_amount(new_id, data)

        # id2 = data[2]
        # id3 = data[3]
        # data = self.get_data_from_response(id2)
        # self.update_amount(id2, data)

        # data = self.get_data_from_response(id3)
        # self.update_amount(id3, data)
        

# vk
token = '08f8682608f8682608f86826850bec68c4008f808f868266ca567b35dc8f37858cb4172'
version = 5.92
first_id = 155632877


popo = 1



# Создаем экземпляр приложения
app = SixDegreesApp()

# Добавляем людей и связи между ними
app.add_person("Андрей")
app.add_person("Борис")
app.add_person("Василий")
app.add_person("Галина")
app.add_person("Дмитрий")
app.add_person("Дмитрий")
app.add_person("Путин")
app.add_person("Дмитрий")
app.add_person("Дмитрий")
app.add_connection("Андрей", "Борис")
app.add_connection("Борис", "Василий")
app.add_connection("Василий", "Галина")
app.add_connection("Галина", "Дмитрий")


# З
# app.run("Дмитрий", "Андрей")

app.popopo(first_id)
print(len(app.connections))