import requests


def send_remove_book(book_title: str):
    url = f'http://localhost:3333/{book_title}'
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data={})

    if response.status_code == 200:
        print("Resposta do servidor: ", response.json())
    else:
        print("Erro: ", response.status_code, response.text)


if __name__ == "__main__":
    send_remove_book(book_title="O Senhor dos Anéis")
