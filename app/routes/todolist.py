from flask import Blueprint, request, jsonify
from services.todolist_service import TodoList

todo_bp = Blueprint('todolist', __name__)

todos = TodoList()

@todo_bp.route("/todos/getTodosById", methods=["GET"])
def get_todo_by_id():
    id = request.args.get("id")
    
    got_todo = todos.get_todo_by_id(id)
    if not got_todo:
        return jsonify({"error" : "invalid id"})
    return got_todo

@todo_bp.route("/todos/getTodos", methods=["GET"])
def get_todo():
  status = request.args.get("status", "all")
  if status in ["open", "done", "all"]:
    return todos.get_todos(status)
  return jsonify({
    'error': f"invalid status {status}. Must be on of 'open', 'done', or 'all'",
    'message': "invalid request"
  }), 400

@todo_bp.route("/todos/addTodo", methods=["POST"])
def add_todo():
    data = request.json

    if "todo_item" not in data or "description" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'todo_item' and 'description'" }), 401
   
    todos.add(data["todo_item"], data["description"])
    return "Added todo", 201

@todo_bp.route("/todos/removeTodo", methods=["DELETE"])
def remove_todo():
    data = request.json

    if "todo_id" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id'"}), 401
    
    was_deleted = todos.remove(data["todo_id"])

    if not was_deleted:
        return jsonify({"error" : "id doesn't exist"}), 401

    return "deleted todo", 200

@todo_bp.route("/todos/editTodo", methods=["PATCH"])
def edit_todo():
    data = request.json

    if "todo_id" not in data or "new_name" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id', 'new_name'"}), 401
    
    was_edited = todos.edit(data["todo_id"], data["new_name"])

    if not was_edited:
        return jsonify({"error" : "id doesn't exist"}), 401
    
    return "new name updated", 200

@todo_bp.route("/todos/updateStatusTodo", methods=["PATCH"])
def update_status_todo():
    data = request.json

    if "todo_id" not in data or "status" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id', 'status"}), 401
    
    was_updated = todos.update_status(data["todo_id"], data["status"])

    if not was_updated:
        return jsonify({"error" : "id doesn't exist"}), 401

    return "updated status", 200
