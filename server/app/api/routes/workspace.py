from fastapi import APIRouter
from app.schemas.workspace import CreateWorkspaceInput, CreateWorkspaceResponse, GetAllWorkspaceInput, GetAllWorkspaceResponse
from app.db.session import SessionDep

router = APIRouter(tags=["workspace"])

@router.post("/workspaces", response_model=CreateWorkspaceResponse)
async def create_workspace(req: CreateWorkspaceInput, session: SessionDep):
    pass

@router.get("/workspaces", response_model=GetAllWorkspaceResponse)
async def get_all_workspace(req: GetAllWorkspaceInput, session: SessionDep):
    pass