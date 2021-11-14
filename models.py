import pydantic


class NewThought(pydantic.BaseModel):
    content: str
    recaptcha_token: str


class Thought(pydantic.BaseModel):
    creation_date: int
    last_updated: int
    content: str
