from pydantic import BaseModel

class CreatedWithPublicIdAndLinkResponse(BaseModel):
    public_id: str
    link: str