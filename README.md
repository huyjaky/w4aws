# Section 1
| Thông tin | Chi tiết |
| :--- | :--- |
| **Số nhóm** | [Điền số nhóm của bạn] |
| **Tên thành viên** | [Điền tên các thành viên trong nhóm] |
| **LLM** | [Ví dụ: Claude 3 Sonnet via Bedrock] |
| **Embedding** | [Ví dụ: Claude 3 Sonnet via Bedrock] |
| **Framework sử dụng** | [Ví dụ: LangChain / Bedrock Agents / raw API] |

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

# Section 4 — Per-Level Evidence

------------------------------------------------------------------------

## 🔹 Level 1 --- Basic RAG Retrieval

### ✅ Câu trả lời đúng (Screenshot Output)

<img width="1043" height="435" alt="image" src="https://github.com/user-attachments/assets/d3cc6775-9bb8-4d45-b599-e890424bc798" />
> Ví dụ: Câu trả lời có **trích dẫn source document** rõ ràng (ví dụ:
> "Theo tài liệu ServicePolicy_v2.pdf...")

------------------------------------------------------------------------

### 🔍 Bằng chứng Retrieval đã xảy ra

> \[Chèn 1 screenshot log / dashboard\]

**Bằng chứng cần thể hiện:** - System thực hiện retrieve từ Qdrant
(Hybrid Search) - Query embedding được tạo - Top-k chunks được trả về -
Metadata (source document, score) - Retrieved chunks được đưa vào prompt
trước khi gọi LLM

Ví dụ log:

    [Retriever] Hybrid search executed
    Query: "What is API rate limit?"
    Top 3 chunks returned
    Source: service_policy_v2.pdf
    Score: 0.82

➡ Chứng minh LLM không tự đoán mà đã nhận context thật từ RAG pipeline.

------------------------------------------------------------------------

## 🔹 Level 2 --- Multi-document Synthesis / Conflict Resolution

### ✅ Screenshot Output

<img width="1084" height="360" alt="image" src="https://github.com/user-attachments/assets/4d4c7afe-1416-47d9-860a-003e5533d290" />

Ví dụ: - Doc A: API rate limit = 500\
- Doc B (newer version): API rate limit = 1000\
- System trả lời đúng: **1000**

------------------------------------------------------------------------

### 🔎 System xử lý conflict như thế nào?
> \[Chụp ảnh config top k hybrid search của Rag\]
> \[Giải quyết config 2 versions (improve system prompt như nào)\]
-   Hybrid search trả về nhiều documents
-   Agent sử dụng metadata (version / timestamp) để ưu tiên document mới
    hơn
-   LLM được cung cấp cả hai context và được prompt yêu cầu resolve
    conflict

Ví dụ log:

    Retrieved:
    - service_policy_v1.pdf (rate limit: 500)
    - service_policy_v2.pdf (rate limit: 1000)

    LLM instructed to prioritize latest version

➡ Chứng minh system thực sự xử lý multi-doc reasoning.

------------------------------------------------------------------------

## 🔹 Level 3 --- Tool-Augmented Answer (Quan trọng nhất)

### ✅ Screenshot Output

<img width="1909" height="964" alt="image" src="https://github.com/user-attachments/assets/681ddacd-f1e2-47e6-a44b-9fa4e7fe2e66" />

Ví dụ:

> "PaymentGW Q1 cost = \$16,500"

------------------------------------------------------------------------

### 🔧 Bằng chứng Tool được gọi

<img width="547" height="511" alt="image" src="https://github.com/user-attachments/assets/751991df-3e03-4bfa-b4e1-82dd7327296d" />

Log cần thể hiện rõ:

    [Agent] Tool selected: postgresql.executeQuery
    Query executed:
    SELECT SUM(cost)
    FROM billing
    WHERE service = 'PaymentGW'
    AND quarter = 'Q1';

    Tool response:
    16500

Hoặc HTTP tool:

    [Agent] Calling HTTP Tool: /metrics?service=PaymentGW
    Response received:
    { "Q1_cost": 16500 }

➡ Đây là bằng chứng quan trọng nhất: phải thấy tool call + real data
response.

------------------------------------------------------------------------

## 🔹 Level 4 --- Multi-turn Conversation + Memory (Nếu thực hiện)

### ✅ Screenshot Multi-turn Chat

<img width="1087" height="496" alt="image" src="https://github.com/user-attachments/assets/b8267f29-8bab-4c47-a5a2-39c628b6a31a" />
<img width="1087" height="552" alt="image" src="https://github.com/user-attachments/assets/df37d8bb-289d-43fb-958d-f257759afd6f" />
<img width="1073" height="412" alt="image" src="https://github.com/user-attachments/assets/4f19513f-5541-4348-abc1-08d3b0d39990" />
<img width="1081" height="313" alt="image" src="https://github.com/user-attachments/assets/6e4170db-85dc-4706-b108-090dfb8967c7" />


Ví dụ:

User: Q1 cost của PaymentGW là bao nhiêu?\
AI: \$16,500\
User: So với Q2 thì sao?\
AI: Q2 cao hơn 12%

Follow-up tham chiếu lượt trước → chứng minh memory hoạt động.

------------------------------------------------------------------------

### 🧠 Memory Strategy

-   Sử dụng PostgreSQL làm persistent memory
-   Lưu:
    -   user_id
    -   conversation_id
    -   chat history
-   Agent inject lịch sử hội thoại vào prompt mỗi turn
-   Giới hạn số turn để tránh prompt overflow

------------------------------------------------------------------------

# Nếu sử dụng AgentCore

## Architecture Responsibility

  Thành phần                 AgentCore quản lý   Tự build
  -------------------------- ------------------- ----------
  Agent loop                 ✅                  
  Tool orchestration         ✅                  
  Custom Hybrid Search API                       ✅
  PostgreSQL Memory                              ✅
  Observability                                  ✅

------------------------------------------------------------------------

## Annotated Trace Logs

### Example 1 --- RAG-only question

1.  User gửi câu hỏi\
2.  AgentCore quyết định gọi Retriever\
3.  Hybrid Search API được gọi\
4.  Chunks trả về\
5.  LLM synthesize câu trả lời\
6.  Response gửi về user

------------------------------------------------------------------------

### Example 2 --- Tool-augmented question

1.  User hỏi về cost\
2.  Agent reasoning step (Think tool)\
3.  Agent quyết định gọi PostgreSQL tool\
4.  Query executed\
5.  Tool trả về data thật\
6.  LLM format câu trả lời\
7.  Response trả về user

------------------------------------------------------------------------

# Bonus A --- Observability Dashboard

> \[Chèn screenshot dashboard\]

Dashboard hiển thị: - Retrieval step - Tool calls - LLM decision -
Latency từng bước - Token usage

------------------------------------------------------------------------

# Bonus B --- Agent Reasoning (Structured Investigation)

> \[Chèn screenshot reasoning output\]

Ví dụ:

    Step 1: User asking about service cost
    Step 2: Need real billing data
    Step 3: Call PostgreSQL tool
    Step 4: Compute aggregation
    Step 5: Format response

Hiển thị rõ: - Decision-making - Tool selection logic - Intermediate
reasoning

------------------------------------------------------------------------

# ✅ Checklist trước khi nộp

-   [ ] Mỗi level có 1--2 screenshot
-   [ ] Có bằng chứng retrieve thật
-   [ ] Có bằng chứng tool call thật (L3 bắt buộc)
-   [ ] Không chỉ có output cuối
-   [ ] Logs readable, highlight phần quan trọng


