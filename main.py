from fastapi import FastAPI, HTTPException
from models import ItemPayload

app = FastAPI()

grocery_list: dict[int, ItemPayload] = {}

@app.get("/")
def root():
    """
    Root endpoint.

    Returns:
        A dictionary with a message.
    """
    return {"message": "Hello World"}

# Route to add an item to the grocery list
@app.post("/items/{item_name}/{quantity}")
def add_item(item_name: str, quantity: int):
    """
    Add an item to the grocery list.

    Args:
        item_name (str): The name of the item.
        quantity (int): The quantity of the item.

    Returns:
        dict: A dictionary containing the added item.

    Raises:
        HTTPException: If the quantity is less than or equal to 0.
    """
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    # if item already exists, we'll just add the quantity
    # get all item names
    items_ids = {item.item_name: item.item_id if item.item_id is not None else 0 for item in grocery_list.values()}
    
    if item_name in items_ids.keys():
        # get index of item_name in item_ids, which is the item_id
        item_id = items_ids[item_name]
        grocery_list[item_id].quantity += quantity

    # otherwise, create a new item
    else:
        # generate an ID for the item based on the highest ID in the grocery_list
        item_id = max(grocery_list.keys() + [1] if grocery_list else [0])
        grocery_list[item_id] = ItemPayload(
            item_id=item_id,
            item_name=item_name,
            quantity=quantity
        )
        
    return {"item": grocery_list[item_id]}


# Route to list a specific item by ID
@app.get("/items/{item_id}")
def list_item(item_id: int) -> dict[str, ItemPayload]:
    """
    List a specific item by ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: A dictionary containing the item.

    Raises:
        HTTPException: If the item with the given ID is not found in the grocery list.
    """
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"item": grocery_list[item_id]}


# Route to list all items
@app.get("/items")
def list_items() -> dict[str, dict[int, ItemPayload]]:
    """
    List all items in the grocery list.

    Returns:
        dict: A dictionary containing all the items in the grocery list.
    """
    return {"items": grocery_list}


# Route to delete a specific item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, str]:
    """
    Delete a specific item by ID.

    Args:
        item_id (int): The ID of the item to be deleted.

    Returns:
        dict: A dictionary containing a message indicating the success of the deletion.

    Raises:
        HTTPException: If the item with the given ID is not found in the grocery list.
    """
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del grocery_list[item_id]
    return {"message": "Item deleted"}


# Route to remove some quantity of a specific item by ID
@app.delete("/items/{item_id}/{quantity}")
def remove_quantity(item_id: int, quantity: int) -> dict[str, str]:
    """
    Remove some quantity of a specific item by ID.

    Args:
        item_id (int): The ID of the item.
        quantity (int): The quantity to be removed.

    Returns:
        dict: A dictionary containing the result.

    Raises:
        HTTPException: If the item with the given ID is not found in the grocery list.
    """
    if item_id not in grocery_list:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # if quantity to be removed is higher or equal to item's quantity, delete the item
    if grocery_list[item_id].quantity <= quantity:
        del grocery_list[item_id]
        return {"message": "Item deleted"}
    else:
        grocery_list[item_id].quantity -= quantity
    
    return {"result": f"{quantity} items removed."}