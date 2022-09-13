from datetime import datetime

import pydantic


class BaseModel(pydantic.BaseModel):
    created_at: datetime
    updated_at: datetime
