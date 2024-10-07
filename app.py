from flask import Flask, request, jsonify
# from flask_restful import reqparse, abort, Api, Resource
from typing import List, Literal, Optional, TypedDict
import uuid
import random

app = Flask(__name__)
# api = Api(app)

random.seed(123)

def random_uuid():
    return uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)


class TodoItem(TypedDict):
    todo_id: str
    name: str
    description: str
    is_done: bool


def create_todo_item(name: str, description: str) -> TodoItem:
    todo_id = str(random_uuid())
    return {
        "todo_id": todo_id,
        "name": name,
        "description": description,
        "is_done": False,
        }



class TodoList:
    def __init__(self) -> None:
        self.todos: List[TodoItem] = []

    def add(self, todo: str, description: Optional[str] = "") -> None:
        # Create a new todo item
        new_item = TodoItem(create_todo_item(todo, description))
        self.todos.append(new_item)
        return True

    def remove(self, todo_id: str) -> None:
        # Remove a todo item
        for todo in self.todos:
            if todo["todo_id"] == todo_id:
                self.todos.remove(todo)
                return True
        return False

    def edit(self, todo_id: str, new_name: str) -> None:
        # Edit a todo item
        for i in self.todos:
            if i["todo_id"] == todo_id:
                i["name"] = new_name
                return True
        return False

    def update_status(self, todo_id: str, is_done: bool) -> None:
        # Update the status of a todo item
        for todo in self.todos:
            if todo["todo_id"] == todo_id:
                todo["is_done"] = is_done
                return True
        raise KeyError(f"Todo item with ID {todo_id} not found.")

    def get_todos(self, show_completed: Literal["open", "done", "all"]) -> dict:
        # Get all the todo items
        # can also filter by "open" = show all incomplete todos, "done" = show all completed todos, "all" = show all todos
        
        if show_completed == "all":
            return self.todos 

        is_completed = True if show_completed == "done" else False
        todo_list = [todo for todo in self.todos if todo["is_done"] == is_completed]
        return todo_list

    def get_todo_by_id(self, todo_id: str) -> dict:
        # Get a todo item by its id)
        for item in self.todos:
            if item["todo_id"] == todo_id:
                return item
        return False

# kims_todos.add("laundry", "white clothes only")
# kims_todos.get_todos("all")
# kims_todos.update_status('0d4416c4-6844-4bd6-a6df-0961898f5557', True)
# kims_todos.get_todos("all")
# kims_todos.edit('0d4416c4-6844-4bd6-a6df-0961898f5557', "ask Angelo to do laundry")
# kims_todos.get_todos("all")
# kims_todos.add("vape for 2hrs", "mint juice")
# kims_todos.get_todos("open")
# kims_todos.remove('da0d2822-568f-45b3-be29-00e76fc616e0')
# kims_todos.get_todos("all")




todos = TodoList()
todos.add("laundry", "white clothes only")
todos.add("vape for 2 hours", "mint")

# @app.route('/todos/add', methods=['POST'])
# def add_todo():
#     data = request.get_json()
#     name = data.get('name')
#     description = data.get('description', "")
#     todo_list.add(name, description)
#     return jsonify({"message": "Todo item added successfully"}), 201

# @app.route('/todos/delete', methods=['DELETE'])
# def remove_todo():
#   return


@app.route("/todos/getTodosById", methods=["GET"])
def get_todo_by_id():
    id = request.args.get("id")
    
    got_todo = todos.get_todo_by_id(id)
    if not got_todo:
        return jsonify({"error" : "invalid id"})
    return got_todo

@app.route("/todos/getTodos", methods=["GET"])
def get_todo():
  status = request.args.get("status", "all")
  if status in ["open", "done", "all"]:
    return todos.get_todos(status)
  return jsonify({
    'error': f"invalid status {status}. Must be on of 'open', 'done', or 'all'",
    'message': "invalid request"
  }), 400

@app.route("/todos/addTodo", methods=["POST"])
def add_todo():
    data = request.json

    if "todo_item" not in data or "description" not in data:
        return jsonify({ "error": "Bad request. JSON body needs 'todo_item' and 'description'" }), 401
   
    todos.add(data["todo_item"], data["description"])
    return "Added todo", 201

@app.route("/todos/removeTodo", methods=["DELETE"])
def remove_todo():
    data = request.json

    if "todo_id" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id'"}), 401
    
    was_deleted = todos.remove(data["todo_id"])

    if not was_deleted:
        return jsonify({"error" : "id doesn't exist"}), 401

    return "deleted todo", 200

@app.route("/todos/editTodo", methods=["PATCH"])
def edit_todo():
    data = request.json

    if "todo_id" not in data or "new_name" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id', 'new_name'"}), 401
    
    was_edited = todos.edit(data["todo_id"], data["new_name"])

    if not was_edited:
        return jsonify({"error" : "id doesn't exist"}), 401
    
    return "new name updated", 200

@app.route("/todos/updateStatusTodo", methods=["PATCH"])
def update_status_todo():
    data = request.json

    if "todo_id" not in data or "status" not in data:
        return jsonify({ "error" : "Bad request. JSON body needs 'todo_id', 'status"}), 401
    
    was_updated = todos.update_status(data["todo_id"], data["status"])

    if not was_updated:
        return jsonify({"error" : "id doesn't exist"}), 401

    return "updated status", 200

if __name__ == '__main__':
    app.run(debug=True)
