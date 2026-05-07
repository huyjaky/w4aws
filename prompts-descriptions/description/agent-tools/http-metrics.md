**Tool Name**: Get_Service_Metrics
**Description**: Use this tool to retrieve real-time operational metrics for a specific service, including current latency, error rate, and CPU/memory usage. 
**CRITICAL RULES**: 
1. **Jitter Awareness**: The live values returned by this API have a built-in ±5% jitter. Slight fluctuations between multiple calls are normal and should NOT be treated as data contradictions.
2. **Temporal Priority**: This is LIVE data. If these metrics differ from the `daily_metrics` table in the `Postgresql tool`, treat this API's data as the absolute current state and the database as the historical state.
**Input**: `service_name` (string) - The exact, case-sensitive name of the service.
