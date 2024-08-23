from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import json

class BookRemovalServerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Recebendo solicitação para remoção de livro...")
        url_path = self.path
        book_title = url_path.split('/')[1]
        book_title = unquote(book_title)

        books_json = []
        with open('db.json', 'r') as json_file:
            books_json.extend(json.load(json_file))

        books_json_copy = [book for book in books_json]
        try:
            for book in books_json_copy:
                if book['title'] == book_title:
                    books_json.remove(book)

            with open('db.json', 'w', encoding='utf-8') as file:
                json.dump(books_json, file, ensure_ascii=False, indent=4)

            # enviando resposta de SUCESSO
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Livro removido com sucesso"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Resposta enviada com sucesso")
        except ValueError:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "not found", "message": "Este livro não consta na nossa base de dados"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Resposta enviada com sucesso")
        


def run(server_class=HTTPServer, handler_class=BookRemovalServerHandler, port=3333):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor rodando na porta {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()