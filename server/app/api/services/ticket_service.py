from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.ticket import Ticket
from app.schemas.ticket import CreateTicketInput, CreateTicketResponse, UpdateTicketInput, UpdateTicketResponse, PushTicketInput, PushTicketResponse, GetAllTicketResponse, TicketStatus
from sqlalchemy import select, update
from uuid import UUID

class TicketService:
    def __init__(self):
        pass

    async def create(
        self, workspace_id: str, ticket_input: CreateTicketInput, session: AsyncSession
    ) -> CreateTicketResponse:
        #TODO: Integrate LLM API with ticket_input
        ticket = Ticket(workspace_id=workspace_id, title="random", description="random", status="str")
        session.add(ticket)
        await session.commit()
        return CreateTicketResponse(tickets=[ticket])
    
    async def update(
        self, workspace_id: UUID, ticket_id: UUID, ticket_input: UpdateTicketInput, session: AsyncSession
    ) -> UpdateTicketResponse:
        result = await session.execute(select(Ticket).where(Ticket.id == ticket_id, Ticket.workspace_id == workspace_id))

        ticket = result.scalar_one_or_none()
        if ticket is None:
            raise ValueError("Ticket is not found")
        
        update_data = ticket_input.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(ticket, field, value)

        await session.commit()
        await session.refresh(ticket)

        return ticket
    
    async def get_ticket(
        self, workspace_id: UUID, session: AsyncSession
    ) -> GetAllTicketResponse:
        result = await session.execute(select(Ticket).where(Ticket.workspace_id == workspace_id))

        tickets = result.scalars().all()

        return GetAllTicketResponse(
            tickets=tickets
        )

    async def push_ticket(
        self, workspace_id: UUID, ticket_input: PushTicketInput, session: AsyncSession
    ) -> PushTicketResponse:
        result = await session.execute(
            update(Ticket).where(Ticket.workspace_id == workspace_id, Ticket.id.in_(ticket_input.ticket_ids)).values(status=TicketStatus.PROCESSING).returning(Ticket)
        )
        successful_tickets = result.scalars().all()

        if not successful_tickets:
            raise ValueError("All tickets failed to push")

        success = set(s.id for s in successful_tickets)
        failed = set(ticket_input.ticket_ids) - success

        await session.commit()

        return PushTicketResponse(pushed=list(success), failed=list(failed))
