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
<img width="1814" height="381" alt="image" src="https://github.com/user-attachments/assets/3512dee0-915b-4afc-be44-f4d1be0a176c" />
<img width="1386" height="526" alt="image" src="https://github.com/user-attachments/assets/fe9f8c62-cec5-499f-b8f8-8b7b315a2969" />


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

### 1. Khởi tạo & Lấy dữ liệu (Trigger & Input)
- **Webhook1 (POST):** Điểm neo (Trigger) nhận yêu cầu HTTP POST để bắt đầu luồng xử lý nạp dữ liệu.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/079c5cd3-40ba-4fc1-ad87-c34bb481c961" />

- **Read/Write Files from Disk (Read File(s) From Disk):** Quét và đọc các tệp tài liệu từ ổ đĩa cục bộ để chuẩn bị xử lý.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/157d9ef4-d2c1-49a3-88d2-e1d63a90daed" />

- **Loop Over Items:** Node tạo vòng lặp (iterator). Nó nhận danh sách các file từ bước trước và phân nhánh quá trình xử lý: đưa từng file vào nhánh `loop` để xử lý chi tiết, và chuyển sang nhánh `done` khi đã duyệt qua hết tất cả các file.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/444f0db0-e630-470d-8fca-f63f8aec02e4" />

- 
### 2. Xử lý dữ liệu văn bản 
- **Getting text from files (Extract From Text File):** Trích xuất nội dung chữ (raw text) từ tệp tài liệu đang được lặp.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/d0c38f42-4082-43db-83eb-f31b8ba8a2c6" />

- **Augment data:** Nút này (thường chứa script) dùng để gán thêm siêu dữ liệu (metadata) hoặc làm giàu thông tin cho văn bản, ví dụ như thêm tên nguồn, ngày tạo, hoặc phân loại tài liệu.
- **Chunking:** Cắt nội dung văn bản dài thành các đoạn nhỏ hơn (chunks). (token: 1024, overlap: 200)
- **Limit:** Giới hạn số lượng item đi qua luồng. <img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/c915fa5b-018c-41c1-a309-8b82fe7177bb" />

### 3. Vector hóa & Lưu trữ
* **Vector Store Processor:** Xử lý các chunk văn bản cùng với metadata tương ứng (như đường nối chỉ ra). Nút này đóng vai trò chuẩn bị định dạng dữ liệu (hoặc kết nối mô hình embedding) trước khi nạp vào cơ sở dữ liệu vector. <img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/1b2c900c-12d7-46f9-beff-3590f09212f9" />

* **Aggregate:** Gom nhóm (batch) các item riêng lẻ lại thành một mảng (array) lớn. Việc này giúp giảm số lượng request gửi đi ở bước tiếp theo, tối ưu hóa hiệu suất mạng.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/022da3a0-b6ac-4744-9d78-dcc4b3ce0f5b" />

* **Upsert (POST):** Thực hiện một HTTP Request (địa chỉ IP nội bộ `192.168.31...`) để chèn mới hoặc cập nhật (upsert) hàng loạt các chunk/vector dữ liệu vào Vector Database (QDrant). Sau khi hoàn tất, luồng sẽ quay ngược lại **Loop Over Items** để tiếp tục với file tiếp theo.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/df301229-69cf-4b6c-a3e4-91bac9a4ffe4" />

### 4. Dọn dẹp & Phản hồi (Nhánh `done`)
- **mv files:** Xử lý hậu kỳ sau khi tất cả các tệp đã được vector hóa xong. Thường dùng để di chuyển (move) các file gốc sang một thư mục khác (như `archived` hoặc `processed`) để tránh việc nạp trùng lặp trong tương lai.
- **Respond to Webhook1:** Trả về mã trạng thái HTTP (ví dụ: 200 OK) cho hệ thống đã gọi Webhook ban đầu, xác nhận rằng toàn bộ quá trình xử lý và nạp dữ liệu đã hoàn tất thành công.<img width="1888" height="876" alt="image" src="https://github.com/user-attachments/assets/b26e6f2f-48e9-4489-bf13-4d96973857af" />

Dưới đây là phần mô tả Data Flow (Luồng dữ liệu) chi tiết được thiết kế dựa trên sơ đồ kiến trúc của bạn. Bạn có thể copy nội dung này và dán trực tiếp vào mục **3. Data Flow** trong Section 2 của file Evidence Pack.

## Data flow

1. **Tiếp nhận yêu cầu (Input):** Dữ liệu đầu vào đi vào hệ thống thông qua `Webhook` (từ các hệ thống bên ngoài) hoặc trigger `When chat message received` (từ giao diện người dùng).
2. **Xử lý ngữ cảnh (Context & Memory):** `AI Agent` tiếp nhận yêu cầu và ngay lập tức truy vấn component `Memory` để lấy lịch sử các lượt hội thoại trước đó, tạo chuỗi ngữ cảnh đầy đủ cho câu hỏi hiện tại.
3. **Phân tích & Lập kế hoạch (Reasoning):** Agent định tuyến yêu cầu cùng ngữ cảnh đến LLM (`claude opus 4.6`). LLM sẽ phân tích ý định của người dùng và quyết định xem có thể trả lời trực tiếp hay cần sử dụng công cụ (Tool). Component `Think` có thể được kích hoạt ở bước này để thiết lập các bước tư duy logic cho các truy vấn phức tạp.
4. **Thực thi công cụ (Tool Invocation - Nếu có):** Nếu cần truy xuất dữ liệu để trả lời, LLM điều phối Agent gọi các tools tương ứng. Agent có thể truy vấn cơ sở dữ liệu qua `Postgresql tool`, tìm kiếm tài liệu dạng text qua `RAG`, hoặc lấy dữ liệu hệ thống thời gian thực qua nhóm `HTTP tools` (ví dụ: /metrics, /status). Dữ liệu thô từ tools được trả ngược lại cho LLM.
5. **Tổng hợp & Trả kết quả (Output):** LLM tổng hợp và xử lý dữ liệu thu thập được từ các tools để tạo ra câu trả lời chính xác cuối cùng. Câu trả lời này được Agent chuyển đến node `Respond to Webhook` để trả kết quả về cho hệ thống hoặc người dùng đã gửi yêu cầu ban đầu.

## Video System đang chạy [Link video](https://drive.google.com/file/d/1E6ZxlYYH3vwFcjnJEXJ09ydyLLxNTi_0/view?usp=sharing)

# Section 4 — Per-Level Evidence

------------------------------------------------------------------------

## Level 1 --- Basic RAG Retrieval

### Câu trả lời đúng (Screenshot Output)

<img width="1043" height="435" alt="image" src="https://github.com/user-attachments/assets/d3cc6775-9bb8-4d45-b599-e890424bc798" />

------------------------------------------------------------------------

### Bằng chứng Retrieval đã xảy ra

- gọi embedding <img width="1047" height="135" alt="image" src="https://github.com/user-attachments/assets/dcd7eeff-6720-454f-87ef-278837287c7d" />
<img width="695" height="778" alt="image" src="https://github.com/user-attachments/assets/7e47e7d9-d4c4-4f41-8ee0-2732b4a193b3" />
<img width="643" height="186" alt="image" src="https://github.com/user-attachments/assets/e0b2862f-135a-4b9b-b063-912d451ceb8f" />

------------------------------------------------------------------------

## Level 2 --- Multi-document Synthesis / Conflict Resolution

### Screenshot Output

<img width="1084" height="360" alt="image" src="https://github.com/user-attachments/assets/4d4c7afe-1416-47d9-860a-003e5533d290" />

Ví dụ: - Doc A: API rate limit = 500
- Doc B (newer version): API rate limit = 1000
- System trả lời đúng: **1000**

------------------------------------------------------------------------

### System xử lý conflict như thế nào?
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

## Level 3 --- Tool-Augmented Answer (Quan trọng nhất)

### Screenshot Output

<img width="1909" height="964" alt="image" src="https://github.com/user-attachments/assets/681ddacd-f1e2-47e6-a44b-9fa4e7fe2e66" />

Ví dụ:

> "PaymentGW Q1 cost = \$16,500"

------------------------------------------------------------------------

### Bằng chứng Tool được gọi

<img width="929" height="245" alt="image" src="https://github.com/user-attachments/assets/7659b58b-3864-40e4-b69c-b00befa30636" />
<img width="638" height="251" alt="image" src="https://github.com/user-attachments/assets/add2393c-226c-4fcc-9d2a-8eecea914166" />

------------------------------------------------------------------------

## Level 4 --- Multi-turn Conversation + Memory (Nếu thực hiện)

### Screenshot Multi-turn Chat


<img width="1173" height="532" alt="image" src="https://github.com/user-attachments/assets/b8ef7cf3-a59f-4cdc-ba0d-342875b95e62" />
<img width="1173" height="532" alt="image" src="https://github.com/user-attachments/assets/94aff012-2af3-4bcb-aaca-9130c25a79a2" />
-> thể hiện lịch sử chat trong session với AI và human làm chủ thể 

<img width="1087" height="496" alt="image" src="https://github.com/user-attachments/assets/b8267f29-8bab-4c47-a5a2-39c628b6a31a" />
<img width="1087" height="552" alt="image" src="https://github.com/user-attachments/assets/df37d8bb-289d-43fb-958d-f257759afd6f" />
<img width="1073" height="412" alt="image" src="https://github.com/user-attachments/assets/4f19513f-5541-4348-abc1-08d3b0d39990" />
<img width="1081" height="313" alt="image" src="https://github.com/user-attachments/assets/6e4170db-85dc-4706-b108-090dfb8967c7" />

------------------------------------------------------------------------

### Memory Strategy
<img width="1089" height="802" alt="image" src="https://github.com/user-attachments/assets/27a5c639-8811-41da-875d-5e037c598201" />

-   Sử dụng PostgreSQL làm persistent memory
-   Lưu:
    -   session_id
    -   message

------------------------------------------------------------------------

# Bonus A --- Observability Dashboard

<img width="417" height="580" alt="image" src="https://github.com/user-attachments/assets/1fd6592e-46a4-4888-bd5a-407e1fe3de6b" />
<img width="407" height="472" alt="image" src="https://github.com/user-attachments/assets/b98b0ddd-3aac-48d5-9d6d-d8640abd2ab5" />
<img width="414" height="541" alt="image" src="https://github.com/user-attachments/assets/0e54d218-379f-4d92-9a01-8f903f8a9081" />
<img width="415" height="466" alt="image" src="https://github.com/user-attachments/assets/9fa6be39-d886-4098-88d7-8cedab576582" />
<img width="405" height="626" alt="image" src="https://github.com/user-attachments/assets/c854bc91-dfdb-45be-b2f1-565bc6a46a9a" />


Dashboard hiển thị: - Retrieval step - Tool calls - LLM decision -
Latency từng bước - Token usage

------------------------------------------------------------------------

# Bonus B --- Agent Reasoning (Structured Investigation)

<img width="417" height="565" alt="image" src="https://github.com/user-attachments/assets/c228a1a5-dfe5-472f-ba27-effc11db100a" />
<img width="421" height="517" alt="image" src="https://github.com/user-attachments/assets/d559afca-7d53-4086-ba43-7050bd75d114" />
<img width="405" height="403" alt="image" src="https://github.com/user-attachments/assets/69bf1d66-7811-46d1-94b9-aff665d730ad" />
<img width="404" height="617" alt="image" src="https://github.com/user-attachments/assets/d157a918-203f-41bf-b776-0be7ce554809" />


Ví dụ:

    Step 1: User asking about service cost
    Step 2: Need real billing data
    Step 3: Call PostgreSQL tool
    Step 4: Compute aggregation
    Step 5: Format response

Hiển thị rõ: - Decision-making - Tool selection logic - Intermediate
reasoning

------------------------------------------------------------------------

