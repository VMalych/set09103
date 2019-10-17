from flask import Flask, request
app = Flask(__name__)

@app.route("/hello/")
def hello():
    name = request.args.get('name', '')
    if name == '':
        return "no param supplied"
    else:
        return "Hello %s" % name

@app.route("/add/<int:first>/<int:second>")
def add(first, second):
    return str(first+second)

@app.route("/account/", methods=['POST', 'GET'])
def account():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save('static/uploads/upload.png')
        return "File Uploaded"
    else:
        page ='''
        <html>
        <body>
        <form action="" method="post" name="form" enctype="multipart/form-data">
            <input type="file" name="datafile" />
            <input type="submit" name="submit" id="submit"/>
        </form>
        </body>
        <html>
        '''

        return page, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
