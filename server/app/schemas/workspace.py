from pydantic import BaseModel
from typing import List


class Workspace(BaseModel):
    id: str
    user_id: str
    repo_id: str
    repo_name: str
    project_id: str
    project_name: str
    context: str
    ai_generated_project_summary: str
    created_at: str
    updated_at: str


class CreateWorkspaceInput(BaseModel):
    repo_id: str
    repo_name: str
    project_id: str
    project_name: str
    context: str


class CreateWorkspaceResponse(Workspace):
    pass


class GetAllWorkspaceInput(BaseModel):
    user_id: str


class GetAllWorkspaceResponse(BaseModel):
    workspaces: List[Workspace]
