from datetime import datetime

from pydantic import BaseModel

from app.core.models.organization import Department


class DepartmentResponse(BaseModel):
    id: int
    name: str

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(model: Department):
        response = DepartmentResponse(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

        return response