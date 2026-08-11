from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []
next_id = 1

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200

@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not isinstance(title, str):
        return jsonify({"error": "field 'title' is required and must be a string"}), 400

    todo = {"id": next_id, "title": title, "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json(silent=True) or {}
    todo = next((t for t in todos if t["id"] == todo_id), None)

    if todo is None:
        return jsonify({"error": "todo not found"}), 404

    if "title" in data:
        if not isinstance(data["title"], str):
            return jsonify({"error": "'title' must be a string"}), 400
        todo["title"] = data["title"]

    if "done" in data:
        if not isinstance(data["done"], bool):
            return jsonify({"error": "'done' must be a boolean"}), 400
        todo["done"] = data["done"]

    return jsonify(todo), 200

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)

    if todo is None:
        return jsonify({"error": "todo not found"}), 404

    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)