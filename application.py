from flask import Flask, jsonify, abort, request, render_template
import model
import random
from flask_accept import accept
from collections import Counter
import dicttoxml

app = Flask(__name__)
text_db = model.FDataBase()
dict_lines = None
file_name = None
list_longest = None


def random_line():
    '''
    :return: Random line from currently uploaded file
    '''
    random.seed()
    global dict_lines
    try:
        if dict_lines is not None:
            rnd_line = int(random.choices(list(dict_lines.keys()))[0])
            msg = dict_lines[rnd_line]
            return msg
        else:
            msg = "File wasn't uploaded"
            return msg
    except:
        return "Error in lines dictionary"


def find_frequent_letter(line):
    '''
    :return: Most frequent letter in a line and not a space
    '''
    ct = Counter(str(line).lower())
    most_commons = ct.most_common(1)
    most_frequent = most_commons[0]
    if most_frequent[0] == ' ':
        return most_frequent[1]
    else:
        return most_frequent[0]


def find_twenty(lines: list, n: int) -> list:
    '''
    Longest N(20) lines in a file
    :param lines: list of sorted lines by their length
    :param n: amount of lines
    :return: first N lines, or exixting amount of lines
    '''
    list_twenty = []
    count = 0
    for item in lines:
        if count < n:
            list_twenty.append(item[1])
            count += 1
    print(list_twenty)
    return list_twenty


def random_line_info():
    '''
    :return: Founds a random line and some information about it
    '''
    random.seed()
    try:
        if dict_lines is not None:
            rnd_line = int(random.choices(list(dict_lines.keys()))[0])
            msg = dict_lines[rnd_line]
            most_frequent_letter = find_frequent_letter(msg)
            print(msg, rnd_line, most_frequent_letter)
            return msg, rnd_line, most_frequent_letter
        else:
            msg = "File wasn't uploaded"
            return msg
    except:
        return "Error in lines dictionary"


@app.route("/", methods=["POST", "GET"])
def index():
    msg = f'Use menu for some information'
    return render_template("index.html", ok=msg)


@app.route("/upload", methods=["POST", "GET"])
def file_upload():
    '''
    Getting file data. Upload in the database, basic analysys of the text lines.
    :return: rendered template
    '''

    msg = ''
    if request.method == "POST":
        file = request.files["file"]
        try:
            if file.filename.endswith(".txt"):
                file_lns = file_analysis(file)
                return render_template("upload.html", ok='Upload successful', client_data=file_lns, mult=False, )
            else:
                return render_template("upload.html", msg="Only txt files allowed")
        except FileNotFoundError as e:
            msg = f'File Not Found Error: {e}'

    return render_template("upload.html", msg=msg)


def file_analysis(file):
    '''
     Getting file data. Upload in the database, basic analysis of the text lines.
     :return: rendered template
     '''

    data = str(file.read())
    file_lns = data.split('\\r\\n')

    global file_name, dict_lines
    file_name = file.filename

    # Index of each line zip lines
    index_lines = [i for i in range(len(file_lns))]
    dict_lines = dict(zip(index_lines, file_lns))

    # Number of chars in a line + lines
    index_lines = [len(file_lns[i]) for i in range(len(file_lns))]

    global list_longest
    list_longest = sorted(dict(zip(index_lines, file_lns)).items(), reverse=True)
    text_db.insert_file_query(file.filename, list(zip(index_lines, file_lns)))

    return file_lns


@app.route('/app')
@accept('text/html',
        'application/json',
        'application/xml',
        'application/*')
def get_one_line():
    '''
    Getting one line in the last uploaded file with accept types
        'text/html',
        'application/json',
        'application/xml',
        'application/*'
    PLEASE, test this method with a REST client
    :return:
    '''

    type_accept = request.headers.get('Accept')
    if type_accept == 'application/json':
        return jsonify({'Random string': random_line()})
    elif type_accept == 'text/html':
        return render_template("index.html", client_data=random_line(), mult=False)
    elif type_accept == 'application/xml':
        return dicttoxml.dicttoxml({'Random string': random_line()})
    elif type_accept == 'application/*':
        return render_template("index.html", client_data=random_line_info(), mult=True)
    else:
        abort(404)


@app.route('/twenty_lines')
def twenty_lines():
    '''
    Getting twenty lines in the last uploaded file
    :return: rendered template, list of the longest lines
    '''

    print('twenty_lines')
    try:
        lines = find_twenty(list_longest, 20)
        return render_template("index.html", client_data=lines, mult=True)
    except:
        abort(405)


@app.route('/hundred_lines')
def hundred_lines():
    '''
    :return: rendered template, list of no more than 100 longest lines
    '''

    try:
        lines = text_db.hundred_rows_query(table="texts", amount=100)
        return render_template("index.html", client_data=lines, mult=True, ok="List of longest lines")
    except:
        abort(405)


@app.route('/backwards')
def backwards():
    '''
    :return: rendered template, line with characters backward
    '''
    return render_template("index.html", client_data=random_line()[::-1], mult=False)


@app.errorhandler(400)
def bad_request(error):
    '''
    :return: Error message
    '''
    return render_template("index.html", msg='Error. Bad request')


@app.errorhandler(404)
def not_found(error):
    '''
    :return: Error message for testing Accept headers
    '''
    return render_template("index.html", msg="Sorry, method can't be tested here. "
                                             "Please, download a file and use a REST client")


@app.errorhandler(405)
def not_found(error):
    '''
    :return: Method is not allowed or can't be used
    '''
    return render_template("index.html", msg="Method is not allowed or can't be used")



if __name__ == '__main__':
    app.run(debug=True)