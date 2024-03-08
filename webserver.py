from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

tasklist =  ["Task 1", "Task 2", "Task 3"]

def response_200(self) :
    self.send_response(200)
    self.send_header("content-type", "text/html")
    self.end_headers()

def response_301(self, whereto) :
    self.send_response(301)
    self.send_header("content-type", "text/html")
    self.send_header("Location", whereto)
    self.end_headers()


class requestHandler(BaseHTTPRequestHandler) :
    def do_GET(self):
        #if self.path.endswith("") :
        #    response_200(self)
        #    output = ""
        #    output += "<html><body>"
        #    output += "<h1>Task List<h1>"
        #    output += "</html></body>"
        #    self.wfile.write(output.encode())

        if self.path.endswith("/tasklist") :
            response_200(self)

            output = ""
            output += "<html><body>"
            output += "<h1>Task List<h1>"
            output += '<h3><a href="/tasklist/new">Add New Task</a></h3>'
            for task in tasklist :
                output += task + " "
                output += '<a href="/tasklist/%s/remove">X</a>' % task
                output += "</br>"
            output += "</html></body>"
            self.wfile.write(output.encode())

        if self.path.endswith("/new") :
            response_200(self)

            output = ""
            output += "<html><body>"
            output += "<h1>Add New Task<h1>"

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="task" type="text" placeholder="Add new task">'
            output += '<input type="submit" value="add">'
            output += "</form>"
            output += "</html></body>"
            self.wfile.write(output.encode())

        if self.path.endswith("/remove") :
            listidpath = self.path.split("/")[2]
            response_200(self)

            output = ""
            output += "<html><body>"
            output += "<h1>Remove task: %s<h1>" %listidpath.replace("%20", " ")
            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/%s/remove">' % listidpath
            output += '<input type="submit" value="Remove">'
            output += "</form>"
            output += '<a href="/tasklist">Cancel</a>'
            output += "</html></body>"
            self.wfile.write(output.encode())

    def do_POST(self) :
        if self.path.endswith("/new") :
            ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
            pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
            if ctype =="multipart/form-data" :
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get("task")
                tasklist.extend(new_task)
            response_301(self, "/tasklist")

        if self.path.endswith("/remove") :
            listidpath = self.path.split("/")[2]
            ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
            if ctype == "multipart/form-data" :
                list_item = listidpath.replace("%20", " ")
                tasklist.remove(list_item)
            response_301(self, "/tasklist")


def main() :
    PORT = 8000
    server = HTTPServer(("", PORT), requestHandler)
    print(f"Server is running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()