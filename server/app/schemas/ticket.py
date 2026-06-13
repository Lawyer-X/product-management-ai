from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID
from enum import StrEnum


class TicketStatus(StrEnum):
    PROCESSING = "processing"
    PUSHED = "pushed"


class Ticket(BaseModel):
    id: UUID
    workspace_id: UUID
    title: str
    description: str
    github_issue_id: str | None
    status: TicketStatus
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
    pushed: List[UUID]
    failed: List[UUID]

class GetAllTicketResponse(BaseModel):
    tickets: List[Ticket]