def test_health_check(client):
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_create_task(client):
	response = client.post(
		"/tasks",
		json={
			"title": "Test task",
			"description": "Created by pytest",
		},
	)

	assert response.status_code == 201

	data = response.json()

	assert data["title"] == "Test task"
	assert data["description"] == "Created by pytest"
	assert data["completed"] is False
	assert "id" in data



def test_get_tasks(client):
	client.post(
		"/tasks",
		json = {
			"title": "Task 1",
			"description": "First task"
		},
	)

	client.post(
		"/tasks",
		json = {
			"title": "Task 2",
			"description": "Second task",
		},
	)

	response = client.get("/tasks")

	assert response.status_code == 200

	data = response.json()

	assert len(data) == 2
	assert data[0]["title"] == "Task 1"
	assert data[1]["title"] == "Task 2"


def test_get_task(client):
	create_response = client.post(
		"/tasks",
		json = {
			"title": "Specific task",
			"description": "Task for GET by ID",
		},
	)

	task_id = create_response.json()["id"]

	response = client.get(f"/tasks/{task_id}")

	assert response.status_code == 200

	data = response.json()

	assert data["id"] == task_id
	assert data["title"] == "Specific task"


def test_get_nonexistent_task(client):
	response = client.get("/tasks/999999")

	assert response.status_code == 404
	assert response.json() == {"detail": "Task not found"}


def test_update_task(client):
	create_response = client.post(
		"/tasks",
		json={
			"title": "Old title",
			"description": "Old description",
		},
	)

	task_id = create_response.json()["id"]

	response = client.put(
		f"/tasks/{task_id}",
		json={
			"title": "Updated title",
			"description": "Updated description",
			"completed": True,
		},
	)

	assert response.status_code == 200

	data = response.json()

	assert data["id"] == task_id
	assert data["title"] == "Updated title"
	assert data["description"] == "Updated description"
	assert data["completed"] is True


def test_delete_task(client):
	create_response = client.post(
		"/tasks",
		json={
			"title": "Task to delete",
			"description": "This task should be deleted",
		},
	)

	task_id = create_response.json()["id"]

	response = client.delete(f"/tasks/{task_id}")

	assert response.status_code == 204

	get_response = client.get(f"/tasks/{task_id}")

	assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
	response = client.delete("/tasks/999999")

	assert response.status_code == 404
	assert response.json() == {"detail": "Task not found"}
