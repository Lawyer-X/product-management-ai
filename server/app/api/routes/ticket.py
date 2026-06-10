from fastapi import APIRouter
from app.db.session import SessionDep
from app.schemas.ticket import CreateTicketInput, CreateTicketResponse, UpdateTicketInput, UpdateTicketResponse, PushTicketInput, PushTicketResponse, GetAllTicketInput, GetAllTicketResponse
from uuid import UUID

router = APIRouter(tags=["ticket"], prefix="/workspaces/{workspace_id}",)

@router.post("/tickets", response_model=CreateTicketResponse)
async def create_ticket(workspace_id: UUID, req: CreateTicketInput, session: SessionDep):
    pass

@router.patch("/tickets/{ticket_id}", response_model=UpdateTicketResponse)
async def update_ticket(workspace_id: UUID, ticket_id: UUID, req: UpdateTicketInput, session: SessionDep):
    pass

@router.post("/tickets/push", response_model=PushTicketResponse)
async def push_ticket(workspace_id: UUID, req: PushTicketInput):
    pass

@router.get("/tickets", reponse_model=GetAllTicketResponse)
async def get_all_tickets(workspace_id: UUID, req: GetAllTicketInput):
    pass


