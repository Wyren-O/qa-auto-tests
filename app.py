from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()  

class User(BaseModel):
    id: int | None = None
    name: str
    age: int

users = []
next_id = 1

@app.post("/users", status_code=201)
def create_user(user: User):
    global next_id
    user.id = next_id
    next_id += 1
    users.append(user)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: User):
    for user in users:
        if user.id == user_id:
            user.name = user_data.name
            user.age = user_data.age
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
