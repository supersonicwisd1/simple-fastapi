from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}
# @app.get('/')
# def home():
#     return {'Data':"Test"}

# @app.get("/about")
# def about():
#     return {'Data': 'About'}

# @app.get('/get-item/{item_id}')
# def get_item(item_id: int):
#     return inventory[item_id]

# add description of the path
@app.get('/get-item/{item_id}')
def get_item(item_id: int = Path(None, description="The id of the wanted item", gt=0)):
    return inventory[item_id]

#multiple path parameter
# @app.get('/get-item/{item_id}/{name}')
# def get_item(item_id: int, name: str = None):
#     return inventory[item_id]

# compulsory query parameters
@app.get('/get-by-name')
def get_item(name: str = Query(None, description="name of the item", max_length=10, min_length=2)):
    for item_id in inventory:
        if inventory[item_id]['name'] == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#Optional Query parameter
#from typing import Optional <-- that should be imported
# @app.get('/get-by-name')
# def get_item(name: Optional[str] = None):
#     for item_id in inventory:
#         if inventory[item_id]['name'] == name:
#             return inventory[item_id]
#     return{'Data': 'Not found'}

# Optional and compulsory
# @app.get('/get-by-name')
# def get_item( *, name: Optional[str] = None, test: int): #You can also write test first before the optional(name) for it to work or just add * and comma
#     for item_id in inventory:
#         if inventory[item_id]['name'] == name:
#             return inventory[item_id]
#     return{'Data': 'Not found'}

# Query and Path parameters together
# @app.get('/get-by-name/{item_id}')
# def get_item( *, item_id: int, name: Optional[str] = None, test: int): #You can also write test first before the optional(name) for it to work or just add * and comma
#     for item_id in inventory:
#         if inventory[item_id].name == name:
#             return inventory[item_id]
#     # return{'Data': 'Not found'} you can also do this but not professional

#     #import status and HTTPException from fastapi
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # raise HTTPException(status_code=404, detail="Item name not found") this can also be use if you don import status

#REquest Parameter
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID not found")

    inventory[item_id] = item # you can use longcut "inventory[item_id] = {'name': item.name, 'brand': item.brand, 'price': item.price} 
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item ID does not exist") 
    
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
        
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code=400, detail="Item does not exist.")

    del inventory[item_id]
    return {"Success": "Item deleted!"}