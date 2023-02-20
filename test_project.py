import responses
from model import FDataBase

'''
It's just a start of writing tests for the web-service, 
It wasn't mentioned in a challenge description, so I didn't work for a full coverage.
And made a few tests just for basic methods and requests.
'''


def test_home(client):
    response = client.get("/")
    assert b"<title>Client test</title>" in response.data


def test_txt_file(client, app):
    response = client.post("/upload", data={"test.pdf"})

    with app.app_context():
        assert not FDataBase.connection == None
        assert b"Only txt files allowed" in response.data


def test_file_upload(client, app):
    response = client.post("/upload", data={"test.txt"})

    with app.app_context():
        test_result = FDataBase.execute_query("SELECT line_data FROM texts")
        assert "too excellent" in test_result
        assert b"How can my muse want subject to invent" in response.data


def test_line_backwards(client, app):
    response = client.post("/backwards")

    with app.app_context():
        assert response.data in '?esraeher ot repap ragluv ' \
                                'yreve roF tnellecxe oot ,tnemugra teews nwo enihT esrev ' \
                                'ym otni ts’ruop taht ,ehtaerb tsod uoht elihW ,' \
                                'tnevni ot tcejbus tnaw esum ym nac woH'


def test_find_twenty(client, app):
    response = client.post("/twenty_lines")
    amount = len(response.data)
    with app.app_context():
        assert len(response.data[0]) >= len(response.data[1])
        assert len(response.data[0]) >= len(response.data[2])
        assert len(response.data[1]) >= len(response.data[amount])


def test_hundred_lines(client, app):
    response = client.post("/hundred_lines")
    amount = len(response.data)
    with app.app_context():
        assert amount > 0
        assert "List of longest lines" in response.data


def test_get_one_line(client, app):
    response = client.post("/app")

    with app.app_context():
        assert response.status_code == 404
