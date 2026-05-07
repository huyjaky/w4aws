const { RecursiveCharacterTextSplitter } = require('@langchain/textsplitters');

// 1. Cấu hình (Configuration)
const maxTokens = 1024; // Kích thước tối đa mỗi chunk
const overlap = 200;    // Số ký tự chồng lấp giữa các chunk

// 2. Lấy đầu vào (chỉ lấy văn bản từ item đầu tiên)
// Hỗ trợ cả trường hợp dữ liệu nằm ở trường 'text' hoặc 'data'
const inputText = $input.first().json.text || $input.first().json.data || '';

// Kiểm tra xem có văn bản không
if (!inputText) {
  return [{ json: { error: 'Không tìm thấy văn bản để cắt (No text found).' } }];
}

try {
  // 3. Khởi tạo bộ cắt văn bản
  const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: maxTokens,
    chunkOverlap: overlap,
  });

  // 4. Thực hiện cắt văn bản (sử dụng await vì đây là hàm bất đồng bộ)
  const chunks = await textSplitter.splitText(inputText);
  const results = chunks.map((chunk, index) => {
    return {
      json: {
        chunk_id: index + 1,
        text: chunk
      }
    };
  });

  return results;

  /* 
  // CÁCH B: Nếu bạn muốn trả về giống y hệt lúc trước (1 item chứa 1 mảng mảng segments) 
  // thì xóa đoạn CÁCH A ở trên đi và dùng dòng này:
  // return [{ json: { segments: chunks } }];
  */

} catch (error) {
  // Xử lý lỗi nếu việc cắt văn bản thất bại
  return [{ json: { error: error.message } }];
}
