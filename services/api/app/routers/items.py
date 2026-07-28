from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["items"])

_items = [
    {"id": 1, "name": "Widget A", "price": 9.99},
    {"id": 2, "name": "Widget B", "price": 19.99},
    {"id": 3, "name": "Widget C", "price": 29.99},
]


@router.get("/items")
def list_items():
    return {"items": _items, "count": len(_items)}


@router.get("/items/{item_id}")
def get_item(item_id: int):
    for item in _items:
        if item["id"] == item_id:
            return item
    return {"error": "not found"}
