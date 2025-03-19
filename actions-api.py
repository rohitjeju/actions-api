from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Actions API",
    description="""
    Actions API provides endpoints for managing various types of actions in the system.
    
    ## Features
    * Fetch actionable emails
    * Manage actionable chats
    * Handle pending approvals
    
    ## Authentication
    This API requires authentication using Bearer token.
    """,
    version="1.0.0",
    contact={
        "name": "Rohit Jejurikar",
        "email": "rohitjejurikar@gmail.com",
        "url": "https://www.linkedin.com/in/rohitjejurikar/"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
)

# Pydantic models for request/response
class Action(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Actionable Email",
                "description": "An email that requires user action",
                "price": 0.0
            }
        }

# In-memory database
actions_db = ["Actionable Emails", "Actionable Chats", "Pending Approvals"]

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message with API information
    """
    return {"message": "Welcome to the Actions API"}

@app.get("/actions", response_model=List[Action])
async def get_items():
    """
    Get all available actions in the system.
    
    Returns:
        List[Action]: A list of all actions
        
    Raises:
        HTTPException: If there's an error retrieving the actions
    """
    return actions_db

@app.get("/actions/{item_id}", response_model=Action)
async def get_item(item_id: int):
    """
    Get a specific action by its ID.
    
    Args:
        item_id (int): The unique identifier of the action
        
    Returns:
        Action: The requested action object
        
    Raises:
        HTTPException: If the action is not found (404)
    """
    item = next((item for item in actions_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return item

# @app.post("/actions", response_model=Action)
# async def create_item(item: Action):
#     """
#     Create a new action in the system.
    
#     Args:
#         item (Action): The action object to create
        
#     Returns:
#         Action: The created action object
        
#     Raises:
#         HTTPException: If the action ID already exists (400)
#     """
#     if any(x.id == item.id for x in actions_db):
#         raise HTTPException(status_code=400, detail="Action ID already exists")
#     actions_db.append(item)
#     return item

@app.put("/actions/{action_id}", response_model=Action)
async def update_action(action_id: int, action: Action):
    """
    Update an existing action by its ID.
    
    Args:
        action_id (int): The unique identifier of the action to update
        action (Action): The updated action object
        
    Returns:
        Action: The updated action object
        
    Raises:
        HTTPException: If the action is not found (404)
    """
    index = next((i for i, x in enumerate(actions_db) if x.id == action_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Action not found")
    actions_db[index] = action
    return action

# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     """Delete an Action"""
#     index = next((i for i, x in enumerate(actions_db) if x.id == item_id), None)
#     if index is None:
#         raise HTTPException(status_code=404, detail="Action not found")
#     actions_db.pop(index)
#     return {"message": "Action deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
