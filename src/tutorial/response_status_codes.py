"""
HTTP Response Status Codes
https://fastapi.tiangolo.com/tutorial/response-status-code/
"""

from fastapi import APIRouter, status

router = APIRouter(prefix="/response_status_codes", tags=["HTTP Response Status Codes"])


"""
Basic status codes and descriptions:
• 100 and above are for "Information"
    • rarely use them directly
    • cannot have a body
• 200 and above are for "Successful" responses
    • would use the most
    • 200 is the default status code, which means everything was "OK".
    • 201, "Created" - commonly used after creating a new record in the database.
    • 204, "No Content"
        • used when there is no content to return to the client
        • so the response must not have a body.
• 300 and above are for "Redirection"
    • these status codes may or may not have a body
    • 304, "Not Modified", must not have a body
• 400 and above are for "Client error" responses
    • the second type you would probably use the most
    • 404, "Not Found" response
    • For generic errors from the client, you can just use 400.
• 500 and above are for server errors.
    • almost never use them directly
    • when something goes wrong, it will auto return one of these status codes.
"""


@router.post("/ok/", status_code=200)
async def create_item(name: str):
    return {"name": name}


@router.post("/created/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
