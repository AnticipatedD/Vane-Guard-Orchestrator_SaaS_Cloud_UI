import json
import sys
import os

# Append project root to path for smooth execution tracking
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import WLEProcessDetailsResponse, WLEErrorResponse

def run_local_validation_drill():
    print("=" * 80)
    print("VANE-GUARD ORCHESTRATOR: REQUISITION STREAM VALIDATION DRILL RUNTIME")
    print("=" * 80)

    # 1. Exact replica data context extracted from your verified corporate payload dump
    hiring_sample_payload = {
        "status": "200",
        "data": {
            "creationTime": "2020-07-16T16:34:36Z",
            "description": "This process covers a manager requesting to create a new position or fill an existing position.",
            "executionState": "Active",
            "state": "STATE_RUNNING",
            "lastModificationTime": "2020-07-16T16:34:38Z",
            "name": "Standard Employee Requisition for (Standard HR Open New Position)",
            "piid": "603",
            "caseFolderID": "2126.855fc24f-9414-45f5-a20f-e72de703fe2e",
            "caseFolderServerName": "IBM_BPM_ManagedStore",
            "processTemplateID": "25.c904b3b1-afc1-4698-bf5a-a20892c20275",
            "processTemplateName": "Standard HR Open New Position",
            "processAppName": "Hiring Sample",
            "processAppAcronym": "HSS",
            "processAppID": "2066.9ab0d0c6-d92c-4355-9ed5-d8a05acdc4b0",
            "snapshotName": "Responsive Hiring Sample v18001",
            "snapshotID": "2064.481abfd8-9868-4638-ace0-7932d46958d5",
            "branchID": "2063.1a52abd6-b068-4f9e-91a9-ded9793eb34e",
            "branchName": "Main",
            "snapshotTip": True,
            "dueDate": "2020-07-16T20:34:36Z",
            "comments": [],
            "tasks": [
                {
                    "tkiid": "603",
                    "name": "Submit position request",
                    "status": "Received",
                    "owner": "tw_admin",
                    "assignedTo": "tw_admin",
                    "assignedToDisplayName": "tw_admin",
                    "assignedToID": 9,
                    "assignedToType": "user",
                    "dueTime": "2020-07-16T17:34:37Z",
                    "activationTime": "2020-07-16T16:34:37Z",
                    "atRiskTime": "2020-07-16T17:28:37Z",
                    "clientTypes": ["IBM_WLE_Coach"],
                    "description": "Task: Create position request",
                    "displayName": "Task: Create position request",
                    "isAtRisk": True,
                    "kind": "KIND_PARTICIPATING",
                    "lastModificationTime": "2020-07-16T16:34:37Z",
                    "originator": "tw_admin",
                    "priority": 30,
                    "startTime": "2020-07-16T16:34:37Z",
                    "state": "STATE_CLAIMED",
                    "piid": "603",
                    "processInstanceName": "Standard Employee Requisition for (Standard HR Open New Position)",
                    "priorityName": "Normal"
                }
            ],
            "documents": [],
            "variables": {
                "instanceId": "603",
                "skills": None
            },
            "businessData": [
                {
                    "name": "requisition.department",
                    "type": "String",
                    "alias": "Department",
                    "label": "Department",
                    "value": "Finance Operations"
                },
                {
                    "name": "requisition.gmApproval",
                    "type": "Boolean",
                    "alias": "GMApproval",
                    "label": "GM Approval",
                    "value": False
                }
            ],
            "diagram": {
                "step": [
                    {
                        "ID": "bpdid:431b0753c33842e2:3d5457c0:141a2fd3448:-75fb",
                        "name": "Submit position request",
                        "type": "activity",
                        "activityType": "task",
                        "externalID": "1.1bfbbe13-d8a5-4516-88b6-3d1f29f91af3",
                        "lane": "Hiring Manager",
                        "x": 196,
                        "y": 27,
                        "tokenID": "4",
                        "taskID": "603"
                    }
                ],
                "lanes": [
                    {"name": "Hiring Manager", "height": 187, "system": False},
                    {"name": "System", "height": 150, "system": True}
                ]
            },
            "starterId": "2048.9"
        }
    }

    # 2. Simulate standard runtime exception payload context (Matrix testing)
    error_sample_payload = {
        "status": "404",
        "exceptionType": "ProcessInstanceNotFoundException",
        "errorNumber": "BPM_REST_API_E0404",
        "errorMessage": "Process instance with tracking identifier 603 does not exist in the WLE operational cache repository."
    }

    # Execute Parse Phase 1: Verify valid schema extraction match
    try:
        print("[Execution] Simulating 200 OK stream validation input...")
        verified_success_obj = WLEProcessDetailsResponse.parse_obj(hiring_sample_payload)
        print(f" -> SUCCESS: Framework successfully parsed process instance identifier: {verified_success_obj.data.piid}")
        print(f" -> METRICS: Found task list quantity: {len(verified_success_obj.data.tasks)}")
        print(f" -> DIAGRAM: Extracted lane height for system boundary: {verified_success_obj.data.diagram.lanes[1].height}px")
        print(" -> Data structural integrity confirmed without flaws.")
    except Exception as exc:
        print(f" -> SCHEMA ERROR ON SUCCESS SIMULATION: {str(exc)}")

    print("-" * 80)

    # Execute Parse Phase 2: Verify exception model stability match
    try:
        print("[Execution] Simulating 404 Exception matrix stream input...")
        verified_error_obj = WLEErrorResponse.parse_obj(error_sample_payload)
        print(f" -> EXCEPTION REGISTERED: Exception Model Class: '{verified_error_obj.exceptionType}'")
        print(f" -> MESSAGE TEXT: {verified_error_obj.errorMessage}")
        print(" -> Exception management validation drill verified successfully.")
    except Exception as exc:
        print(f" -> SCHEMA ERROR ON ERROR SIMULATION: {str(exc)}")

    print("=" * 80)
    print("ALL CORE SYSTEM DRILLS COMPLETED. REST BACKEND ENGINE STANDBY RECONCILED.")
    print("=" * 80)

if __name__ == "__main__":
    run_local_validation_drill()
