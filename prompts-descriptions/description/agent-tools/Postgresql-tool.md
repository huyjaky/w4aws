**Tool Name**: Postgresql tool
**Description**: Use this tool to query GeekBrain's structured PostgreSQL database. This database contains historical financial data, system performance metrics, incident logs, and SLA targets for the six production services. You must provide a valid PostgreSQL query to execute.

**Database Schema Overview:**
You have read-only access to the following tables. Construct your SQL queries using these exact table and column names:

1. `monthly_costs`: Use for financial tracking, billing, and cost trend analysis.
   - Columns: `id` (SERIAL), `service` (VARCHAR), `month` (VARCHAR, e.g., 'YYYY-MM'), `compute_cost` (NUMERIC), `storage_cost` (NUMERIC), `network_cost` (NUMERIC), `third_party_cost` (NUMERIC), `total_cost` (NUMERIC).

2. `incidents`: Use for finding past system outages, root causes, severities, and resolution times.
   - Columns: `incident_id` (VARCHAR), `service` (VARCHAR), `date` (DATE), `severity` (VARCHAR), `duration_minutes` (INTEGER), `root_cause` (TEXT), `resolution` (TEXT), `team_responsible` (VARCHAR), `reported_by` (VARCHAR).

3. `sla_targets`: Use to check the official Service Level Agreement (SLA) goals for specific metrics.
   - Columns: `id` (SERIAL), `service` (VARCHAR), `metric` (VARCHAR), `target` (NUMERIC), `measurement_window` (VARCHAR).

4. `daily_metrics`: Use to analyze actual system performance, availability, and error rates over time.
   - Columns: `id` (SERIAL), `date` (DATE), `service` (VARCHAR), `latency_p99_ms` (NUMERIC), `error_rate_percent` (NUMERIC), `requests_per_minute` (INTEGER), `availability_percent` (NUMERIC).

**Querying Instructions & Best Practices:**
- When a user asks whether a service met its SLA, you should generate a query that joins or compares data from `daily_metrics` and `sla_targets`.
- Use standard SQL aggregation functions (`AVG()`, `SUM()`, `MAX()`) to analyze trends over time in `monthly_costs` or `daily_metrics`.
- Ensure string comparisons (like the `service` name) are case-sensitive or use `ILIKE` if uncertain.
- Always add a `LIMIT` clause if you expect a massive amount of rows, unless calculating an aggregate.

**Input**: A single, strictly valid PostgreSQL `SELECT` query string (e.g., `SELECT * FROM incidents WHERE service = 'PaymentGateway' ORDER BY date DESC LIMIT 5;`). Do NOT include markdown blocks like ```sql in the input string itself.
