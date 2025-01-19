# ИСАДИЧЕВА Д.А., ДПИ22-1

import socket
import os
import shutil

# Указание рабочей директории для файлового сервера
SERVER_WORK_DIR = os.path.join(os.getcwd(), 'server_docs')
if not os.path.exists(SERVER_WORK_DIR):
    os.makedirs(SERVER_WORK_DIR)


def handle_client_request(request):
    """
    Обрабатывает запрос клиента и выполняет соответствующую команду.
    """
    try:
        request_parts = request.split(' ')
        command = request_parts[0]

        if command == 'pwd':
            # Возвращает путь текущей рабочей директории сервера
            return SERVER_WORK_DIR

        elif command == 'ls':
            # Возвращает список файлов и папок в рабочей директории
            return '; '.join(os.listdir(SERVER_WORK_DIR))

        elif command == 'mkdir':
            # Создает новую директорию
            if len(request_parts) < 2:
                return 'Error: Directory name not specified'
            directory_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            os.makedirs(directory_name, exist_ok=True)
            return f'Directory {request_parts[1]} created'

        elif command == 'rmdir':
            # Удаляет директорию и ее содержимое
            if len(request_parts) < 2:
                return 'Error: Directory name not specified'
            directory_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            if os.path.exists(directory_name) and os.path.isdir(directory_name):
                shutil.rmtree(directory_name)
                return f'Directory {request_parts[1]} removed'
            return 'Error: Directory not found'

        elif command == 'rm':
            # Удаляет файл
            if len(request_parts) < 2:
                return 'Error: File name not specified'
            file_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            if os.path.exists(file_name) and os.path.isfile(file_name):
                os.remove(file_name)
                return f'File {request_parts[1]} removed'
            return 'Error: File not found'

        elif command == 'rename':
            # Переименовывает файл или директорию
            if len(request_parts) < 3:
                return 'Error: Usage rename <old_name> <new_name>'
            old_file_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            new_file_name = os.path.join(SERVER_WORK_DIR, request_parts[2])
            if os.path.exists(old_file_name):
                os.rename(old_file_name, new_file_name)
                return f'File renamed from {request_parts[1]} to {request_parts[2]}'
            return 'Error: File not found'

        elif command == 'upload':
            # Загружает файл с содержимым
            if len(request_parts) < 3:
                return 'Error: Usage upload <filename> <content>'
            file_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            file_content = ' '.join(request_parts[2:])
            with open(file_name, 'w') as file:
                file.write(file_content)
            return f'File {request_parts[1]} uploaded'

        elif command == 'download':
            # Возвращает содержимое указанного файла
            if len(request_parts) < 2:
                return 'Error: File name not specified'
            file_name = os.path.join(SERVER_WORK_DIR, request_parts[1])
            if os.path.exists(file_name) and os.path.isfile(file_name):
                with open(file_name, 'r') as file:
                    return file.read()
            return 'Error: File not found'

        elif command == 'exit':
            # Завершает сеанс
            return 'Goodbye'

        else:
            # Обработка неизвестной команды
            return 'Error: Unknown command'

    except Exception as error:
        return f'Error: {str(error)}'


# Конфигурация сервера
SERVER_PORT = 6666

server_socket = socket.socket()
server_socket.bind(('', SERVER_PORT))
server_socket.listen()
print(f"Сервер запущен. Рабочая директория: {SERVER_WORK_DIR}")

while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключение от: {client_address}")

    client_request = client_connection.recv(1024).decode()
    print(f"Запрос клиента: {client_request}")

    server_response = handle_client_request(client_request)
    client_connection.send(server_response.encode())

    if client_request == 'exit':
        break

client_connection.close()
