import pytest
import model
import application


@pytest.fixture()
def app():
    application.app.run(debug=True)
    with app.app_context():
        test_db = model.FDataBase('flask_db_test', 'texts')

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
