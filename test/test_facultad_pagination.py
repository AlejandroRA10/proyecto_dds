import pytest
from app import create_app, db
from app.models.facultad import Facultad

@pytest.fixture
def app_fixture():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # crear datos de prueba
        f1 = Facultad(nombre='Facultad de Ingeniería', abreviatura='FI')
        f2 = Facultad(nombre='Facultad de Ciencias', abreviatura='FC')
        f3 = Facultad(nombre='Universidad Tecnológica', abreviatura='UT')
        db.session.add_all([f1, f2, f3])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

def test_pagination_filtering(app_fixture):
    client = app_fixture.test_client()
    # buscar por 'Universidad' debería devolver solo f3
    resp = client.get('/api/facultades?page=1&per_page=2&q=Universidad', headers={'Authorization': 'Basic YW1pZ28xOmNsYXZlMQ=='})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'items' in data
    assert data['total'] == 1
    assert len(data['items']) == 1
    assert data['items'][0]['nombre'] == 'Universidad Tecnológica'

    # paginación sin filtro devuelve items paginados
    resp2 = client.get('/api/facultades?page=1&per_page=2', headers={'Authorization': 'Basic YW1pZ28xOmNsYXZlMQ=='})
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert data2['total'] == 3
    assert len(data2['items']) == 2

    # buscar por abreviatura 'UT' debería devolver f3 también
    resp3 = client.get('/api/facultades?q=UT', headers={'Authorization': 'Basic YW1pZ28xOmNsYXZlMQ=='})
    assert resp3.status_code == 200
    d3 = resp3.get_json()
    # puede devolver lista plana o paginado, comprobar que aparece el nombre buscado
    items3 = d3['items'] if 'items' in d3 else d3
    assert any(i['nombre'] == 'Universidad Tecnológica' for i in items3)
