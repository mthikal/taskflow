import pytest
from app.routes import app, reset_store


@pytest.fixture(autouse=True)
def clean_store():
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ── Health ──────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_ok(self, client):
        r = client.get('/health')
        assert r.status_code == 200
        assert r.get_json()['status'] == 'ok'

    def test_health_reports_task_count(self, client):
        client.post('/api/tasks', json={'title': 'x'})
        r = client.get('/health')
        assert r.get_json()['tasks_count'] == 1


# ── GET /api/tasks ───────────────────────────────────────────────────────────

class TestGetTasks:
    def test_empty_list_on_start(self, client):
        r = client.get('/api/tasks')
        assert r.status_code == 200
        assert r.get_json() == []

    def test_returns_created_tasks(self, client):
        client.post('/api/tasks', json={'title': 'Buy groceries'})
        client.post('/api/tasks', json={'title': 'Walk the dog'})
        r = client.get('/api/tasks')
        assert len(r.get_json()) == 2


# ── POST /api/tasks ──────────────────────────────────────────────────────────

class TestCreateTask:
    def test_create_returns_201(self, client):
        r = client.post('/api/tasks', json={'title': 'Write tests'})
        assert r.status_code == 201

    def test_create_assigns_id(self, client):
        r = client.post('/api/tasks', json={'title': 'First task'})
        assert r.get_json()['id'] == 1

    def test_create_stores_title(self, client):
        r = client.post('/api/tasks', json={'title': 'My Task'})
        assert r.get_json()['title'] == 'My Task'

    def test_create_done_is_false(self, client):
        r = client.post('/api/tasks', json={'title': 'New'})
        assert r.get_json()['done'] is False

    def test_create_strips_whitespace(self, client):
        r = client.post('/api/tasks', json={'title': '  Trimmed  '})
        assert r.get_json()['title'] == 'Trimmed'

    def test_create_empty_title_returns_400(self, client):
        r = client.post('/api/tasks', json={'title': ''})
        assert r.status_code == 400

    def test_create_whitespace_only_title_returns_400(self, client):
        r = client.post('/api/tasks', json={'title': '   '})
        assert r.status_code == 400

    def test_create_missing_title_returns_400(self, client):
        r = client.post('/api/tasks', json={})
        assert r.status_code == 400

    def test_create_no_body_returns_400(self, client):
        r = client.post('/api/tasks', content_type='application/json', data='')
        assert r.status_code == 400

    def test_ids_are_sequential(self, client):
        ids = []
        for i in range(3):
            r = client.post('/api/tasks', json={'title': f'Task {i}'})
            ids.append(r.get_json()['id'])
        assert ids == [1, 2, 3]


# ── PATCH /api/tasks/<id> ────────────────────────────────────────────────────

class TestToggleTask:
    def test_toggle_marks_done(self, client):
        tid = client.post('/api/tasks', json={'title': 'T'}).get_json()['id']
        r = client.patch(f'/api/tasks/{tid}')
        assert r.status_code == 200
        assert r.get_json()['done'] is True

    def test_toggle_twice_reverts(self, client):
        tid = client.post('/api/tasks', json={'title': 'T'}).get_json()['id']
        client.patch(f'/api/tasks/{tid}')
        r = client.patch(f'/api/tasks/{tid}')
        assert r.get_json()['done'] is False

    def test_toggle_nonexistent_returns_404(self, client):
        r = client.patch('/api/tasks/999')
        assert r.status_code == 404


# ── DELETE /api/tasks/<id> ───────────────────────────────────────────────────

class TestDeleteTask:
    def test_delete_returns_200(self, client):
        tid = client.post('/api/tasks', json={'title': 'Del me'}).get_json()['id']
        r = client.delete(f'/api/tasks/{tid}')
        assert r.status_code == 200

    def test_delete_removes_task(self, client):
        tid = client.post('/api/tasks', json={'title': 'Gone'}).get_json()['id']
        client.delete(f'/api/tasks/{tid}')
        tasks = client.get('/api/tasks').get_json()
        assert all(t['id'] != tid for t in tasks)

    def test_delete_nonexistent_returns_404(self, client):
        r = client.delete('/api/tasks/999')
        assert r.status_code == 404

    def test_delete_does_not_affect_others(self, client):
        t1 = client.post('/api/tasks', json={'title': 'Keep'}).get_json()['id']
        t2 = client.post('/api/tasks', json={'title': 'Remove'}).get_json()['id']
        client.delete(f'/api/tasks/{t2}')
        tasks = client.get('/api/tasks').get_json()
        assert any(t['id'] == t1 for t in tasks)
        assert len(tasks) == 1
