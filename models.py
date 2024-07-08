from typing import Optional
from pydantic import BaseModel

class ItemPayload(BaseModel):
    """
    Represents the payload for an item.

    Attributes:
        item_id (Optional[int]): The ID of the item (optional).
        item_name (str): The name of the item.
        quantity (int): The quantity of the item.
    """
    item_id: Optional[int]
    item_name: str
    quantity: int