import mongoengine as me
from fastapi import FastAPI, HTTPException
from mongoengine import Document, StringField, IntField

# Conectar a la base de datos MongoDB
me.connect('Beneficios', host='localhost', port=27017)

# Definir el modelo para la colección 'users'
class User(Document):
    user = StringField(required=True)  # Campo que quieres evaluar
    email = StringField(required=True)

# Crear la aplicación FastAPI
app = FastAPI()

# Endpoint para obtener todos los usuarios
@app.get("/users")
async def get_users():
    users = User.objects()
    return list(users)

# Endpoint para obtener un usuario por nombre de usuario
@app.get("/users/{user}")
async def get_user(user: str):
    user_obj = User.objects(user=user).first()
    print(user_obj)
    if not user_obj:
        print("no encontrado:")
        return {"message": "Usuario no encontrado"}
    else:
        print("encontrado:")
        return {"message": "Usuario encontrado", "user": user_obj}

# Endpoint para crear un nuevo usuario
@app.post("/users")
async def create_user(user: str, email: str, age: int = None):
    new_user = User(user=user, email=email, age=age)
    new_user.save()
    return new_user

# Endpoint para actualizar un usuario por nombre de usuario
@app.put("/users/{user}")
async def update_user(user: str, email: str = None, age: int = None):
    user_obj = User.objects(user=user).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    if email:
        user_obj.email = email
    if age:
        user_obj.age = age
    user_obj.save()
    return user_obj

# Endpoint para eliminar un usuario por nombre de usuario
@app.delete("/users/{user}")
async def delete_user(user: str):
    user_obj = User.objects(user=user).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    user_obj.delete()
    return {"message": "User deleted successfully"}