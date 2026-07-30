from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# ==========================================
# 1. OFFICIAL IBM ENUMERATION CONSTRAINTS
# ==========================================

class DocumentType(str, Enum):
    FILE = "FILE"
    URL = "URL"

class RelationshipType(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    DEPENDENT = "DEPENDENT"

class ExecutionState(str, Enum):
    Active = "Active"
    Completed = "Completed"
    Failed = "Failed"
    Suspended = "Suspended"
    Terminated = "Terminated"

class ProcessState(str, Enum):
    STATE_COMPENSATED = "STATE_COMPENSATED"
    STATE_COMPENSATION_FAILED = "STATE_COMPENSATION_FAILED"
    STATE_COMPENSATING = "STATE_COMPENSATING"
    STATE_DELETED = "STATE_DELETED"
    STATE_FAILED = "STATE_FAILED"
    STATE_FAILING = "STATE_FAILING"
    STATE_FINISHED = "STATE_FINISHED"
    STATE_INDOUBT = "STATE_INDOUBT"
    STATE_READY = "STATE_READY"
    STATE_RUNNING = "STATE_RUNNING"
    STATE_SUSPENDED = "STATE_SUSPENDED"
    STATE_TERMINATED = "STATE_TERMINATED"
    STATE_TERMINATING = "STATE_TERMINATING"

class AvailableAction(str, Enum):
    ACTION_ABORT_INSTANCE = "ACTION_ABORT_INSTANCE"
    ACTION_ADD_COMMENT = "ACTION_ADD_COMMENT"
    ACTION_ADD_DOCUMENT = "ACTION_ADD_DOCUMENT"
    ACTION_ADD_HELP_REQUEST = "ACTION_ADD_HELP_REQUEST"
    ACTION_CHANGE_CRITICAL_PATH = "ACTION_CHANGE_CRITICAL_PATH"
    ACTION_CHANGE_INSTANCE_DUEDATE = "ACTION_CHANGE_INSTANCE_DUEDATE"
    ACTION_DELETE_DOCUMENT = "ACTION_DELETE_DOCUMENT"
    ACTION_DELETE_INSTANCE = "ACTION_DELETE_INSTANCE"
    ACTION_DELETE_TOKEN = "ACTION_DELETE_TOKEN"
    ACTION_FIRE_TIMER = "ACTION_FIRE_TIMER"
    ACTION_INJECT_TOKEN = "ACTION_INJECT_TOKEN"
    ACTION_MOVE_TOKEN = "ACTION_MOVE_TOKEN"
    ACTION_RESPOND_HELP_REQUEST = "ACTION_RESPOND_HELP_REQUEST"
    ACTION_RESUME_INSTANCE = "ACTION_RESUME_INSTANCE"
    ACTION_SUSPEND_INSTANCE = "ACTION_SUSPEND_INSTANCE"
    ACTION_UPDATE_DOCUMENT = "ACTION_UPDATE_DOCUMENT"
    ACTION_VIEW_INSTANCE = "ACTION_VIEW_INSTANCE"
    ACTION_VIEW_PROCESS_AUDIT = "ACTION_VIEW_PROCESS_AUDIT"
    ACTION_VIEW_PROCESS_DIAGRAM = "ACTION_VIEW_PROCESS_DIAGRAM"


# ==========================================
# 2. IBM COMPLEX SUB-STRUCTURES
# ==========================================

class Document(BaseModel):
    ID: Optional[str] = Field(None, description="The identifier of the document.")
    ecmID: Optional[str] = Field(None, description="The ECM identifier of the document.")
    type: Optional[DocumentType] = Field(None, description="The type of the document.")
    name: Optional[str] = Field(None, description="The name of the document.")
    date: Optional[datetime] = Field(None, description="The date and time when the document was created.")
    length: Optional[int] = Field(None, description="The size of the document in bytes (FILE only).")
    url: Optional[str] = Field(None, description="The URL of the document (URL only).")
    version: Optional[int] = Field(None, description="The version number of the document.")

class Creator(BaseModel):
    userID: Optional[int] = Field(None, description="User ID of the creator.")
    userName: Optional[str] = Field(None, description="User login name.")
    fullName: Optional[str] = Field(None, description="Full descriptive name of the user.")
    isDisabled: Optional[bool] = Field(False, description="Is user disabled.")

class Relationship(BaseModel):
    id: Optional[str] = None
    type: Optional[RelationshipType] = None
    sourceId: Optional[str] = None
    targetId: Optional[str] = None
    description: Optional[str] = None
    creationDate: Optional[datetime] = None
    lastModified: Optional[datetime] = None
    creator: Optional[Creator] = None

class BusinessDataField(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    alias: Optional[str] = None
    label: Optional[str] = None
    value: Optional[Any] = None

class TaskItem(BaseModel):
    tkiid: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    assignedTo: Optional[str] = None
    assignedToDisplayName: Optional[str] = None
    assignedToID: Optional[int] = None
    assignedToType: Optional[str] = None
    dueTime: Optional[datetime] = None
    activationTime: Optional[datetime] = None
    atRiskTime: Optional[datetime] = None
    clientTypes: Optional[Union[str, List[str]]] = None
    description: Optional[str] = None
    displayName: Optional[str] = None
    isAtRisk: Optional[bool] = None
    kind: Optional[str] = None
    lastModificationTime: Optional[datetime] = None
    originator: Optional[str] = None
    priority: Optional[int] = None
    startTime: Optional[datetime] = None
    state: Optional[str] = None
    piid: Optional[str] = None
    processInstanceName: Optional[str] = None
    priorityName: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class StepLine(BaseModel):
    to: Optional[str] = None
    points: Optional[str] = None
    name: Optional[str] = None

class DiagramStep(BaseModel):
    ID: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    activityType: Optional[str] = None
    externalID: Optional[str] = None
    lane: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None
    lines: Optional[List[StepLine]] = None
    tokenID: Optional[Union[str, List[str]]] = None
    taskID: Optional[str] = None

class DiagramLane(BaseModel):
    name: Optional[str] = None
    height: Optional[int] = None
    system: Optional[bool] = None

class ProcessDiagram(BaseModel):
    step: Optional[List[DiagramStep]] = None
    lanes: Optional[List[DiagramLane]] = None


# ==========================================
# 3. ROOT EXCEPTION AND CLIENT RESPONSE TYPE
# ==========================================

class WLEErrorResponse(BaseModel):
    """Maps HTTP Status Codes 400, 401, 404, 406, 500 runtime exceptions."""
    status: str = Field(description="The status of the failed API call.")
    exceptionType: str = Field(description="The classname associated with the exception.")
    errorNumber: str = Field(description="Message ID of the exception.")
    errorMessage: str = Field(description="Message text of the exception.")
    errorMessageParameters: Optional[List[str]] = None
    programmersDetails: Optional[Dict[str, Any]] = None


# ==========================================
# 4. CORE REQUISITION SUCCESS DATA MODEL
# ==========================================

class ProcessDetailsPayload(BaseModel):
    creationTime: Optional[datetime] = None
    description: Optional[str] = None
    richDescription: Optional[str] = None
    executionState: Optional[ExecutionState] = None
    state: Optional[ProcessState] = None
    lastModificationTime: Optional[datetime] = None
    name: Optional[str] = None
    piid: Optional[str] = None
    caseFolderID: Optional[str] = None
    caseFolderServerName: Optional[str] = None
    processTemplateID: Optional[str] = None
    processTemplateName: Optional[str] = None
    processAppName: Optional[str] = None
    processAppAcronym: Optional[str] = None
    processAppID: Optional[str] = None
    snapshotName: Optional[str] = None
    snapshotID: Optional[str] = None
    branchID: Optional[str] = None
    branchName: Optional[str] = None
    snapshotTip: Optional[bool] = None
    dueDate: Optional[datetime] = None
    tasks: Optional[List[TaskItem]] = None
    documents: Optional[List[Document]] = None
    businessData: Optional[List[BusinessDataField]] = None
    variables: Optional[Dict[str, Any]] = None
    data: Optional[str] = Field(None, description="Raw BPD internal data layout.")
    relationship: Optional[List[Relationship]] = None
    diagram: Optional[ProcessDiagram] = None
    starterId: Optional[str] = None

class WLEProcessDetailsResponse(BaseModel):
    """Complete container for standard 200 OK responses."""
    status: str = "200"
    data: ProcessDetailsPayload
