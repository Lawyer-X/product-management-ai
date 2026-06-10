from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class Ticket(BaseModel):
    id: UUID
    workspace_id: UUID
    title: str
    description: str
    github_issue_id: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class CreateTicketInput(BaseModel):
    prompt: str


class CreateTicketResponse(BaseModel):
    tickets: List[Ticket]


class UpdateTicketInput(BaseModel):
    title: str | None
    description: str | None

UpdateTicketResponse = Ticket


class PushTicketInput(BaseModel):
    ticket_ids: List[UUID]


class PushTicketResponse(BaseModel):
    pushed: List[Ticket]
    failed: List[Ticket]