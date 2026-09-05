import sys
import os
import pytest


# Add backend folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

import app as app_module


# Fake DynamoDB Table
class FakeTable:
    def __init__(self):
        self.items = []

    def scan(self):
        return {
            "Items": self.items
        }

    def put_item(self, Item):
        self.items.append(Item)

    def update_item(
        self,
        Key,
        UpdateExpression,
        ExpressionAttributeValues,
        ReturnValues
    ):
        task_id = Key["task-id"]

        for item in self.items:
            if item["task-id"] == task_id:

                if ":title" in ExpressionAttributeValues:
                    item["title"] = ExpressionAttributeValues[":title"]

                if ":completed" in ExpressionAttributeValues:
                    item["completed"] = ExpressionAttributeValues[":completed"]

                return {
                    "Attributes": item
                }

    def delete_item(self, Key):
        task_id = Key["task-id"]

        self.items = [
            item for item in self.items
            if item["task-id"] != task_id
        ]


# Flask Test Client + Fake DynamoDB
@pytest.fixture
def client(monkeypatch):

    fake_table = FakeTable()

    monkeypatch.setattr(
        app_module,
        "table",
        fake_table
    )

    with app_module.app.test_client() as client:
        yield client


# Test Home
def test_home(client):

    response = client.get("/")

    assert response.status_code == 200


# Test Get Tasks
def test_get_tasks(client):

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json == []


# Test Create Task
def test_create_task(client):

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker"
        }
    )

    assert response.status_code == 201

    data = response.json

    assert data["title"] == "Learn Docker"
    assert data["completed"] is False
    assert "task-id" in data


# Test Update Task
def test_update_task(client):

    # Create task first
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn AWS"
        }
    )

    task_id = create_response.json["task-id"]

    # Update task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json["completed"] is True


# Test Delete Task
def test_delete_task(client):

    # Create task first
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to Delete"
        }
    )

    task_id = create_response.json["task-id"]

    # Delete task
    response = client.delete(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 200
    assert response.json["message"] == "Task deleted successfully"