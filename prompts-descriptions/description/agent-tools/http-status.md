**Tool Name**: Get_Service_Status
**Description**: Use this tool to fetch the LIVE uptime percentage and any active, ongoing alerts for a specific GeekBrain service. 
**CRITICAL RULE**: This tool provides the real-time state. If the output of this tool contradicts the historical documentation retrieved from `RAG` or past metrics from the `Postgresql tool`, you MUST prioritize this live data to describe the "Current State" and highlight the difference.
**Input**: `service_name` (string) - The exact, case-sensitive name of the service.
