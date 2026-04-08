"""Todo application with TRL-annotated functions.

Each function has a <trl> block that specifies its exact behavior.
The LLM reads these as formal obligations, not suggestions.
"""

# <trl>FUNCTION create_todo SHALL VALIDATE RECORD input
#   THEN WRITE VALID RECORD TO DATA todos.
# FUNCTION create_todo SHALL_NOT WRITE INVALID RECORD.</trl>
def create_todo(title: str, todos: list[dict]) -> dict:
    if not title or not title.strip():
        raise ValueError("Title is required")
    todo = {
        "id": len(todos) + 1,
        "title": title.strip(),
        "done": False,
    }
    todos.append(todo)
    return todo


# <trl>FUNCTION list_todos SHALL READ ALL RECORD FROM DATA todos
#   THEN FILTER BY RECORD state IF RECORD state EXISTS.</trl>
def list_todos(todos: list[dict], done: bool | None = None) -> list[dict]:
    if done is None:
        return todos
    return [t for t in todos if t["done"] == done]


# <trl>FUNCTION complete_todo SHALL MATCH RECORD BY INTEGER id
#   THEN WRITE state=VALID TO RECORD.
# IF RECORD SHALL_NOT EXISTS THEN THROW EXCEPTION.</trl>
def complete_todo(todo_id: int, todos: list[dict]) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return todo
    raise KeyError(f"Todo {todo_id} not found")


if __name__ == "__main__":
    store: list[dict] = []

    create_todo("Learn TRL vocabulary", store)
    create_todo("Add AGENT.md to my project", store)
    create_todo("Write TRL specifications", store)

    complete_todo(1, store)

    print("All todos:")
    for t in list_todos(store):
        status = "done" if t["done"] else "pending"
        print(f"  [{status}] {t['title']}")

    print("\nPending:")
    for t in list_todos(store, done=False):
        print(f"  [ ] {t['title']}")
