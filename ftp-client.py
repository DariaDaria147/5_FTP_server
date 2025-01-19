# ИСАДИЧЕВА Д.А., ДПИ22-1

import socket

# Конфигурация клиента
SERVER_HOST = 'localhost'  # Адрес сервера
SERVER_PORT = 6666         # Порт сервера

while True:
    # Ввод команды от пользователя
    client_request = input('ftp> ')

    # Создание сокета и подключение к серверу
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Отправка команды серверу
    client_socket.send(client_request.encode())

    # Прием и отображение ответа от сервера
    server_response = client_socket.recv(1024).decode()
    print(server_response)

    # Закрытие соединения
    client_socket.close()

    # Выход из цикла при команде 'exit'
    if client_request == 'exit':
        break
