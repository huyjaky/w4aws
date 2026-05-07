# Section 1
| Thông tin | Chi tiết |
| :--- | :--- |
| **Số nhóm** | GROUP 10 |
| **Tên thành viên** | 
1. XB-DN26-001 — Lê Trần Tuấn Khanh
2. XB-DN26-009 — Trần Mạnh Trường
3. XB-DN26-048 — Trần Mạnh Cường
4. XB-DN26-052 — Nguyễn Đức Hảo
5. XB-DN26-057 — Lê Văn Hải
6. XB-DN26-078 — Phan Đức Huy
7. XB-DN26-082 — Lê Viết Quốc Hưng
8. XB-DN26-129 — Huỳnh Xuân Hậu
9. XB-DN26-131 — Nguyễn Thị Mến
10. XB-DN26-132 — Trần Quốc Hùng |
| **LLM sử dụng** | anthropic.claude-opus-4-6-v1 |
| **Framework sử dụng** | n8n / Bedrock |

---

# Section 2 — Architecture Overview

## System architecture diagram

### Agent
<img width="1581" height="734" alt="image" src="https://github.com/user-attachments/assets/6114221f-3fdc-46ae-b578-4cea0340a48f" />

### Nạp RAG 
<img width="1802" height="318" alt="image" src="https://github.com/user-attachments/assets/64ce7a90-85cb-4935-bdac-883833f7e5bf" />


## Danh sách component

### 1. Nhóm Trigger & Output (Luồng dữ liệu chính)
- *Webhook (POST)*: Node nhận các yêu cầu HTTP POST từ các hệ thống bên ngoài để kích hoạt luồng xử lý, dùng để gọi AGENT.
<img width="1871" height="863" alt="image" src="https://github.com/user-attachments/assets/d632d570-48fa-4e7c-b668-7ba1c2a6d171" />

- When chat message received: Trigger kích hoạt luồng khi người dùng gửi một tin nhắn mới qua giao diện chat.
<img width="1871" height="863" alt="image" src="https://github.com/user-attachments/assets/d014023d-577d-4b5e-b41f-29fbbb0b01c2" />

- AI Agent: Component trung tâm điều phối toàn bộ hệ thống. Nó tiếp nhận câu hỏi, kết nối với LLM, quản lý bộ nhớ (Memory), và quyết định xem nên gọi công cụ (Tool) nào để tìm kiếm hoặc xử lý dữ liệu trước khi đưa ra câu trả lời cuối cùng.
<img width="722" height="859" alt="image" src="https://github.com/user-attachments/assets/5e749dac-dce5-40ca-9fc6-d4b55d8370ee" />


- Respond to Webhook: Node trả về kết quả (dữ liệu hoặc câu trả lời của AI Agent) cho hệ thống/người dùng đã gọi Webhook ban đầu.

### 2. Nhóm Core Dependencies (Gắn vào AI Agent)
- claude opus 4.6 (Model): Mô hình ngôn ngữ lớn (LLM) đóng vai trò là "bộ não" (Chat Model) cung cấp khả năng xử lý ngôn ngữ tự nhiên và suy luận cho AI Agent.
- Memory (PostgreSQL): Component quản lý bộ nhớ, giúp AI Agent lưu trữ ngữ cảnh và lịch sử các đoạn hội thoại trước đó (phục vụ cho multi-turn conversation).

### 3. Nhóm Tools (Các công cụ AI Agent có thể sử dụng)
- Postgresql tool (executeQuery): Công cụ cho phép AI Agent kết nối và thực thi trực tiếp các câu lệnh truy vấn (Query) vào cơ sở dữ liệu PostgreSQL để lấy hoặc thao tác dữ liệu.
- RAG: Hệ thống Retrieval-Augmented Generation. Cung cấp cho Agent khả năng tìm kiếm và trích xuất ngữ cảnh/tài liệu từ các nguồn tri thức (Vector DB, Knowledge base).
- Think: Một công cụ hỗ trợ Agent trong các tác vụ cần tư duy sâu hoặc phân tích logic (reasoning step) trước khi gọi các tool khác hoặc trả lời.
- Nhóm HTTP tools: Cụm các API endpoint được cung cấp dưới dạng tool để Agent tra cứu thông tin hệ thống theo thời gian thực, bao gồm:
  - `/services`: Tra cứu thông tin các dịch vụ.
  - `/status`: Kiểm tra trạng thái hoạt động của hệ thống.
  - `/metrics`: Truy xuất các số liệu đo lường hiệu suất.
  - `/incidents`: Lấy danh sách các sự cố đang xảy ra.
  - `/incidents/{service_name}`: Lấy thông tin sự cố chi tiết của một dịch vụ cụ thể.
