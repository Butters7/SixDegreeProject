# Импортируем необходимые библиотеки
import networkx as nx
import tkinter as tk

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
        self.root = tk.Tk()

        # Создаем элементы интерфейса
        self.label1 = tk.Label(self.root, text="Введите имя первого человека:")
        self.label1.pack()
        self.entry1 = tk.Entry(self.root)
        self.entry1.pack()

        self.label2 = tk.Label(self.root, text="Введите имя второго человека:")
        self.label2.pack()
        self.entry2 = tk.Entry(self.root)
        self.entry2.pack()

        self.button = tk.Button(self.root, text="Найти кратчайший путь", command=self.find_shortest_path)
        self.button.pack()

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

    # Метод для поиска кратчайшего пути между двумя людьми в графе
    def find_shortest_path(self):
        name1 = self.entry1.get()
        name2 = self.entry2.get()
        person1 = self.get_person(name1)
        person2 = self.get_person(name2)
        shortest_path = nx.shortest_path(self.graph, person1, person2)
        print(f"Кратчайший путь между {name1} и {name2}: {[node.name for node in shortest_path]}")

    # Метод для запуска приложения
    def run(self):
        self.root.mainloop()

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
app.run()
