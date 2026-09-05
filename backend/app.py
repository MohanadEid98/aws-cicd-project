from flask_cors import CORS
from flask import Flask, jsonify, request
import boto3
import uuid
app = Flask(__name__)
CORS(app)

dynamodb = boto3.resource ("dynamodb",
region_name="us-east-1")

table = dynamodb.Table("tasks")


tasks = [
    {
        "id": 1,
        "title": "Learn Docker",
        "completed": False
    },
    {
        "id": 2,
        "title": "Learn AWS",
        "completed": False
    }
]


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Task Management API"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/tasks")
def get_tasks():
    response = table.scan()

    return jsonify(response["Items"])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    new_task = {
        "task-id": str(uuid.uuid4()),
        "title": data["title"],
        "completed": False
    }

    table.put_item(Item=new_task)

    return jsonify(new_task), 201
@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    update_expression = []
    expression_values = {}

    if "title" in data:
        update_expression.append("title = :title")
        expression_values[":title"] = data["title"]

    if "completed" in data:
        update_expression.append("completed = :completed")
        expression_values[":completed"] = data["completed"]

    if not update_expression:
        return jsonify({
            "error": "No data provided to update"
        }), 400

    response = table.update_item(
        Key={
            "task-id": task_id
        },
        UpdateExpression="SET " + ", ".join(update_expression),
        ExpressionAttributeValues=expression_values,
        ReturnValues="ALL_NEW"
    )

    return jsonify(response["Attributes"])

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    table.delete_item(
        Key={
            "task-id": task_id
        }
    )

    return jsonify({
        "message": "Task deleted successfully"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)