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


## Danh sách component *Agent*

### 1. Nhóm Trigger & Output (Luồng dữ liệu chính)
- *Webhook (POST)*: Node nhận các yêu cầu HTTP POST từ các hệ thống bên ngoài để kích hoạt luồng xử lý, dùng để gọi AGENT.<img width="1871" height="863" alt="image" src="https://github.com/user-attachments/assets/d632d570-48fa-4e7c-b668-7ba1c2a6d171" />

- When chat message received: Trigger kích hoạt luồng khi người dùng gửi một tin nhắn mới qua giao diện chat.<img width="1871" height="863" alt="image" src="https://github.com/user-attachments/assets/d014023d-577d-4b5e-b41f-29fbbb0b01c2" />

- AI Agent: Component trung tâm điều phối toàn bộ hệ thống. Nó tiếp nhận câu hỏi, kết nối với LLM, quản lý bộ nhớ (Memory), và quyết định xem nên gọi công cụ (Tool) nào để tìm kiếm hoặc xử lý dữ liệu trước khi đưa ra câu trả lời cuối cùng. <img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/dadcfe21-b4d9-4bb6-8b11-cb32d17f38c9" />

- Respond to Webhook: Node trả về kết quả (dữ liệu hoặc câu trả lời của AI Agent) cho hệ thống/người dùng đã gọi Webhook ban đầu.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/5bdea4fd-4904-4877-badc-839a93826532" />

### 2. Nhóm Core Dependencies (Gắn vào AI Agent)
- claude opus 4.6 (Model): Mô hình ngôn ngữ lớn (LLM) đóng vai trò là "bộ não" (Chat Model) cung cấp khả năng xử lý ngôn ngữ tự nhiên và suy luận cho AI Agent.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/2998d6c4-bad4-4133-89be-e3432244a7f4" />

- Memory (PostgreSQL): Component quản lý bộ nhớ, giúp AI Agent lưu trữ ngữ cảnh và lịch sử các đoạn hội thoại trước đó (phục vụ cho multi-turn conversation).<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/7e13c385-2ff1-4ba7-b45d-d07b147a4a99" />

### 3. Nhóm Tools (Các công cụ AI Agent có thể sử dụng)
- Postgresql tool (executeQuery): Công cụ cho phép AI Agent kết nối và thực thi trực tiếp các câu lệnh truy vấn (Query) vào cơ sở dữ liệu PostgreSQL để lấy hoặc thao tác dữ liệu.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/9374bd86-45aa-4e66-bce4-34951b4f2696" />

- RAG (QDrant): Hệ thống Retrieval-Augmented Generation sử dụng *Hybrid search*.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/6fe909b6-4018-470b-bd64-489d1ff48c7b" />
  - vì Hyprid search khá đặc thù nên em wrap Hybrid search vào API để Agent có thể gọi thông qua *HTTP tool* 
 
- Think: Một công cụ hỗ trợ Agent trong các tác vụ cần tư duy sâu hoặc phân tích logic (reasoning step) trước khi gọi các tool khác hoặc trả lời.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/d277a459-524c-48e6-90f7-bdd473fea0ce" />

- Nhóm *HTTP tools*: Cụm các API endpoint được cung cấp dưới dạng tool để Agent tra cứu thông tin hệ thống theo thời gian thực, bao gồm
  - `/services`: Tra cứu thông tin các dịch vụ.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/758c1458-2a5e-4c25-ab9d-b7542a7bd292" />
  - `/status`: Kiểm tra trạng thái hoạt động của hệ thống.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/678a0f1c-7635-4dd0-9a34-188533093ce8" />
  - `/metrics`: Truy xuất các số liệu đo lường hiệu suất.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/56146062-322d-413e-82af-2cfd3ce2843e" />
  - `/incidents`: Lấy danh sách các sự cố đang xảy ra.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/3707376d-95e8-49a3-a79e-b88c508f77f6" />
  - `/incidents/{service_name}`: Lấy thông tin sự cố chi tiết của một dịch vụ cụ thể.<img width="1883" height="878" alt="image" src="https://github.com/user-attachments/assets/824655ff-b0c1-411f-97d6-42d9a71f1826" />

## Danh sách component *Nạp RAG*



