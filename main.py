# Импортируем необходимые библиотеки
from typing import List
import networkx as nx
import requests

# Определяем класс для людей
class Person:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, person):
        self.connections.append(person)


# Определяем класс приложения
class SixDegreesApp:
    def __init__(self):
        # граф находящийся внутри приложения из библиотеки networkx
        self.graph = nx.Graph()
        # счетчик считающий исключения в процессе выполнения программы (пользователь с приватным аккаунтом итд)
        self.exceptions = 0
        # словарь ключ которого состоит из строки связи людей(айдишников) ID1<->ID2, значение равно кол-ву рукопожатий  
        self.connections = {}
        # токен для работы с VK api
        self.token = '08f8682608f8682608f86826850bec68c4008f808f868266ca567b35dc8f37858cb4172'
        # версия VK api
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
    
    # метод который добавляет в словарь self.connections новые связи между человеком и списком людей(его друзей, полученных из vk api) 
    def update_amount(self, id1, ids : List):
        # ids будет private, когда api выдаст ошибку получения друзей пользователя из-за приватного аккаунта
        if ids != 'private':
            self.add_person(id1)
            for id2 in ids:
                self.add_person(id2)
                self.add_connection(id1, id2)
                self.connections[f'{id1}<->{id2}'] = 1
                self.connections[f'{id2}<->{id1}'] = 1
            

    # Метод для поиска длины кратчайшего пути между двумя людьми в графе
    # print_path - для печати пути по нодам
    def shortest_path(self, name1, name2, print_path=False):
        # берем двух людей из графа по значению имени(ID)
        person1 = self.get_person(name1)
        person2 = self.get_person(name2)

        try:
            if f'{name1}<->{name2}' not in self.connections:
                distance = nx.shortest_path_length(self.graph, person1, person2)
                if distance != 0:
                    self.connections[f'{name1}<->{name2}'] = distance
                    self.connections[f'{name2}<->{name1}'] = distance
                    return distance
            else:
                if print_path:
                    path = nx.shortest_path(self.graph, person1, person2)
                    path = [x.name for x in path]
                    print(path)
                return self.connections[f'{name1}<->{name2}']

        # если невозможно найти связь между людьми это идет в исключения
        except nx.exception.NetworkXNoPath:
            print(f'связи между {name1} и {name2} не существует')
            self.exceptions += 1


    # метод для получения ответа от VK api с помощью бибилиотеки request для польвателя с именем first_id
    def create_response(self, first_id):
        return requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'access_token' : self.token,
                                    'v' : self.version,
                                    'user_id' : first_id
                                })
    

    # метод для получения списка друзей(ID-шников) пользователя с именем first_id
    def get_data_from_response(self, first_id):
        response = self.create_response(first_id)
        try:
            data = response.json()['response']['items']
            print(f'пользователь ID{first_id} имеет {len(data)} друзей // using get_data_from_response')
            return data
        except:
            return 'private'


    # метод для получения среднего кол-ва рукопожатий между всеми добавленными пользователями
    def get_average(self):
        return sum(self.connections.values()) / len(self.connections)
                    

    # Алгоритм подразумевает прохождение каждого пользоваетя по каждому пользователю и добавление связи между ними, если таковая имеется
    # сложность O(n^2) - в худшем варианте 
    # оптимизация: при добавлениях пользователей см метод update_amount мы добавляем в словарь connections
    # связи между пользователями. При выполнении алгоритма мы смотрим есть ли в словаре уже такая запись
    # в конце программы мы получаем полностью заполненный всеми связями в графе словарь, значения которого 
    # явл-ся количесвтом рукопожатий между пользователями.
    def process_app(self):
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                key_nodes1 = f'{node1.name}<->{node2.name}'
                key_nodes2 = f'{node2.name}<->{node1.name}'
                if key_nodes1 not in self.connections and key_nodes2 not in self.connections and node1.name != node2.name:
                    self.shortest_path(node1.name, node2.name) 


    # метод, позваоляющий запустить приложение. Он принимает ID первого произвольного пользователя, 
    # добавляет в приложение список его друзей и работает с ними
    # complexity - параметр сложности. позволяет взять меньшее кол-во друзей человека first_id для 
    # быстрого и наглядного выполнения программы
    def simple_run(self, first_id, complexity=382):

        data = self.get_data_from_response(first_id)
        self.update_amount(first_id, data)

        for i in range(len(data) - complexity):
            new_id = data[i]
            new_data = self.get_data_from_response(new_id)
            self.update_amount(new_id, new_data)
        self.process_app()

# объявляем корень приложения, ID, с которого начнется создание графа и получения его друзей в VK
FIRST_ID = 155632877
FRIEND_ID = 697434996
ANOTHER_ID = 269206327

# Создаем экземпляр приложения
app = SixDegreesApp()

# Запуск приложения
app.simple_run(FIRST_ID, complexity=382)

# Информация о выполненной программе 
print(f'добавлено {len(app.connections)} записей в словарь connections')
print(f'граф состоит из {len(app.graph.nodes)} Нод')

print(f'Среднее кол-во рукопожатий {round(app.get_average(), 3)}, исключений встречено: {app.exceptions}')
print(f'путь между ID{FIRST_ID} и ID{FRIEND_ID} : {app.shortest_path(ANOTHER_ID, FRIEND_ID, print_path=True)}')

# Консоль
# пользователь ID155632877 имеет 383 друзей // using get_data_from_response
# пользователь ID971333 имеет 919 друзей // using get_data_from_response
# добавлено 1660232 записей в словарь connections
# граф состоит из 1304 Нод
# Среднее кол-во рукопожатий 2.401, исключений встречено: 0
# [269206327, 155632877, 697434996]
# путь между ID155632877 и ID697434996 : 2

# мой вывод в том, что словарь хорошая идея, но для него на каждую запись связи 
# нужно добавлять две записи ака ID_1<->ID_2 и ID_2<->ID_1
