from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Role(BaseModel):
    name: str
    headers: Dict[str, str] = Field(default_factory=dict)
    cookies: Dict[str, str] = Field(default_factory=dict)

class TargetRequest(BaseModel):
    method: str
    url: str
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Optional[str] = None
    original_role: Optional[str] = None

class AuditConfig(BaseModel):
    target_base_url: str
    roles: List[Role]
    exclude_paths: List[str] = Field(default_factory=list)
    similarity_threshold: float = 0.95
    timeout: int = 15