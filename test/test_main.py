from fastapi.testclient import TestClient

from main import app


TEST_IMAGE_CONTENT = b"test meme image content"
TEST_FILE_DATA = {'image': ("test_meme.png", TEST_IMAGE_CONTENT, 'image/png')}

TEST_MEME_DATA = {'title': "тестовый мем", 'desc': "описание тестового мема"}


client = TestClient(app)


def test_read_memes():
    """Выполнение запроса GET /memes/"""
    response = client.get('/memes/', params={'page': 1, 'limit': 2, 'images': False})

    assert response.status_code == 200

    assert isinstance(response.json(), list)
    for item in response.json():
        assert 'id' in item
        assert 'title' in item
        assert item.get('image') is None


def test_read_memes_validation_error():
    """Валидация запроса GET /memes/"""
    response = client.get('/memes/', params={'page': "invalid", 'limit': "invalid"})

    assert response.status_code == 422
    assert 'detail' in response.json()


def test_create_meme():
    """Выполнение запроса POST /memes/"""
    response = client.post('/memes/', data=TEST_MEME_DATA, files=TEST_FILE_DATA)

    assert response.status_code == 200

    response_json = response.json()
    assert 'id' in response_json
    assert response_json.get('title') == TEST_MEME_DATA['title']
    assert response_json.get('desc') == TEST_MEME_DATA['desc']


def test_create_meme_validation_error():
    """Валидация запроса POST /memes/"""
    test_meme_data = TEST_MEME_DATA.copy()
    test_meme_data['title'] = ""  # обязательное поле!
    response = client.post('/memes/', data=test_meme_data)
    assert response.status_code == 422
    assert 'detail' in response.json()


def test_read_meme_by_id():
    """Выполнение запроса GET /memes/{meme_id}"""
    response = client.post('/memes/', data=TEST_MEME_DATA, files=TEST_FILE_DATA)
    meme_id = response.json().get('id')

    response = client.get(f'/memes/{meme_id}')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get('id') == meme_id
    assert response_json.get('title') == TEST_MEME_DATA['title']
    assert response_json.get('desc') == TEST_MEME_DATA['desc']


def test_read_meme_not_found():
    """Выполнение запроса несуществующего мема"""
    response = client.get('/memes/-1')

    assert response.status_code == 404
    assert 'detail' in response.json()
