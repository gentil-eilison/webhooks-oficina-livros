from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class BookServerHandler(BaseHTTPRequestHandler):
    books = []  # Lista para armazenar os livros

    def _read_books(self):
        with open("db.json", "r") as json_file:
            return json.load(json_file)

    def do_POST(self):
        print("Recebendo solicitação para adicionar livro...")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            book_title = data.get('title')
            book_author = data.get('author')
            book_year = data.get('year')

            if not book_title or not book_author or not book_year:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "error", "message": "Dados do livro incompletos"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print("Erro: Dados do livro incompletos")
                return

            self.books = self._read_books()
            # Adiciona o livro à lista
            self.books.append({
                "title": book_title,
                "author": book_author,
                "year": book_year
            })
            print(f"Livro adicionado: {data}")

            with open("db.json", mode="w", encoding="utf-8") as file:
                json.dump(self.books, file, ensure_ascii=False, indent=4)

            # Enviando resposta de sucesso
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "Livro adicionado com sucesso"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Resposta enviada com sucesso")

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": "Erro ao decodificar JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Erro ao decodificar JSON")

def run(server_class=HTTPServer, handler_class=BookServerHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor rodando na porta {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
