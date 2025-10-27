from fastapi.testclient import TestClient
from app import main
c = TestClient(main.app)
print('GET /')
r = c.get('/')
print('status', r.status_code)
print(r.text[:400])
print('\nGET /flashcards')
r2 = c.get('/flashcards')
print('status', r2.status_code)
try:
    print(r2.json())
except Exception as e:
    print('json error', e)
