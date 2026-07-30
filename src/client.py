import requests
from typing import Optional, Union
from src.models import WLEProcessDetailsResponse, WLEErrorResponse

class IBMProcessRESTClient:
    """
    Vane-Guard Orchestrator core client engine interface.
    Consumes and validates the GET /rest/bpm/wle/v1/process/{instanceId} endpoint.
    """
    def __init__(self, base_url: str, auth_token: str, manifest_data: dict):
        """
        Initializes the client engine and maps enterprise identity keys 
        directly from your verified JSON Schema parameters.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-IBM-Partner-Contract": manifest_data["organization_metadata"]["ibm_partner_contract_id"],
            "X-IBM-Cloud-Account": manifest_data["saas_infrastructure"]["ibm_saas_account_id"],
            "X-Architect-Signature": manifest_data["architect_metadata"]["eu_expert_id"]
        }

    def get_process_instance(
        self, 
        instance_id: str, 
        parts: Optional[str] = None, 
        task_limit: Optional[int] = None, 
        task_offset: Optional[int] = None
    ) -> Union[WLEProcessDetailsResponse, WLEErrorResponse]:
        """
        Executes GET /rest/bpm/wle/v1/process/{instanceId}
        Supported matrix filters: parts, taskLimit, taskOffset.
        """
        url = f"{self.base_url}/rest/bpm/wle/v1/process/{instance_id}"
        
        # Structure parameters strictly according to IBM specification
        params = {}
        if parts:
            params["parts"] = parts
        if task_limit is not None:
            params["taskLimit"] = task_limit
        if task_offset is not None:
            params["taskOffset"] = task_offset

        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Status Matrix validation
            if response.status_code == 200:
                return WLEProcessDetailsResponse.parse_obj(response.json())
                
            elif response.status_code in:
                print(f"[API Error Context] Received failure response status: {response.status_code}")
                return WLEErrorResponse.parse_obj(response.json())
                
            else:
                # Handle unexpected fallback conditions safely
                return WLEErrorResponse(
                    status=str(response.status_code),
                    exceptionType="UnexpectedHTTPStatusException",
                    errorNumber=f"ERR-{response.status_code}",
                    errorMessage=f"Unhandled status text: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            return WLEErrorResponse(
                status="500",
                exceptionType="NetworkConnectionException",
                errorNumber="CONN_ERR_500",
                errorMessage=f"Failed to communicate with IBM Cloud SaaS Gateway: {str(e)}"
            )

