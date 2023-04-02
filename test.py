import pytest
from main import app, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


@pytest.fixture(autouse=True, scope='session')
def prepare_db():
    db.create_all()
    yield
    db.drop_all()


def test_review_add():
    with app.test_client() as client:
        response = client.post('/add-review', json={
            'book_name': 'ASDF',
            'rating': 3,
            'review': 'QWERTY'
        })
        assert response.status_code == 200

def test_review_not_add():
    with app.test_client() as client:
        response = client.post('/add-review', json={
            'book_name': 'ASDF',
            'review': 'QWERTY'
        })
        assert response.status_code == 500

def test_get_book_id():
    with app.test_client() as client:
        response = client.post('/search', json={
            'query': 'ASDF',
        })
        assert response.status_code == 200
        assert int(response.json['book_id']) == 1

#def test_review_add_to_long():
    #with app.test_client() as client:
        #response = client.post('/add-review', json={
            #'book_name': 'ASDF',
            #'rating': 3,
            #'review': 'QWERTY' * 500
            #}


def test_multiple_reviews():
    with app.test_client() as client:
        for i in range (3):
            response = client.post('/add-review', json={
            'book_name': 'ASDF',
            'rating': 3,
            'review': 'QWERTY'
            })

    response = client.get('/most-popular')
    json = response.json
    json_obj = json[0]
    assert json_obj ['review_count'] == 3
