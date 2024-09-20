# Các phương pháp RAG nâng cao

## Adaptive retrievals

Hệ thống bắt đầu bằng cách phân loại truy vấn của người dùng thành một trong bốn loại:

- Thực tế: Truy vấn tìm kiếm thông tin cụ thể, có thể kiểm chứng.
- Phân tích: Các truy vấn yêu cầu phân tích hoặc giải thích toàn diện.
- Ý kiến: Truy vấn về các vấn đề chủ quan hoặc tìm kiếm các quan điểm đa dạng.
- Ngữ cảnh: Các truy vấn phụ thuộc vào ngữ cảnh cụ thể của người dùng.

![alt text](image.png)

### Chiến lược Truy vấn Thực tế

- Tăng cường truy vấn gốc bằng cách sử dụng mô hình ngôn ngữ lớn (LLM) để cải thiện độ chính xác.
Truy xuất tài liệu dựa trên truy vấn đã được tăng cường.
Sử dụng LLM để xếp hạng tài liệu theo mức độ liên quan.

#### prompt
    Enhance this factual query for better information retrieval: {query}

### Chiến lược Phân tích

- Tạo ra nhiều truy vấn phụ bằng LLM để bao quát các khía cạnh khác nhau của truy vấn chính.
- Truy xuất tài liệu cho từng truy vấn phụ.
- Đảm bảo sự đa dạng trong việc chọn lựa tài liệu cuối cùng bằng cách sử dụng LLM.

#### prompt:
    Generate {k} sub-questions for: {query}


### Chiến lược Ý kiến

- Xác định các quan điểm khác nhau về chủ đề bằng LLM.
- Truy xuất tài liệu đại diện cho từng quan điểm.
- Sử dụng LLM để chọn ra một loạt ý kiến đa dạng từ các tài liệu đã truy xuất.

#### prompt:
    Identify {k} distinct viewpoints or perspectives on the topic: {query}

### Chiến lược Ngữ cảnh

- Kết hợp bối cảnh cụ thể của người dùng vào truy vấn bằng LLM.
- Thực hiện truy xuất dựa trên truy vấn có tính ngữ cảnh.
- Xếp hạng tài liệu dựa trên cả mức độ liên quan và bối cảnh của người dùng.

#### prompt:
    Given the user context: {context}
    Reformulate the query to best address the user's needs: {query}


## Corrective RAG Process: Retrieval-Augmented Generation with Dynamic Correction

Quy trình Corrective RAG (Retrieval-Augmented Generation) là một hệ thống truy xuất thông tin và tạo phản hồi tiên tiến. Nó mở rộng cách tiếp cận RAG chuẩn bằng cách đánh giá và điều chỉnh động quá trình truy xuất thông tin, kết hợp sức mạnh của cơ sở dữ liệu vector, tìm kiếm web, và các mô hình ngôn ngữ để cung cấp các phản hồi chính xác và theo ngữ cảnh cho các truy vấn của người dùng.

### Chi tiết Phương pháp
1. Truy xuất Tài liệu:

Thực hiện tìm kiếm tương tự trong chỉ mục FAISS để tìm các tài liệu liên quan.
Truy xuất các tài liệu hàng đầu (mặc định k=3).

2. Đánh giá Tài liệu:

Tính toán điểm liên quan cho từng tài liệu đã truy xuất.
Xác định phương án tốt nhất dựa trên điểm liên quan cao nhất.

3. Thu thập Kiến thức Điều chỉnh:

Nếu điểm liên quan cao (score > 0.7): Sử dụng tài liệu truy vấn.

Nếu điểm liên quan thấp (score < 0.3): Điều chỉnh bằng cách thực hiện tìm kiếm web với một rewrite query.

Nếu điểm liên quan không rõ ràng (0.3 ≤ score ≤ 0.7): Điều chỉnh bằng cách kết hợp tài liệu liên quan nhất với kết quả tìm kiếm web.

4. Xử lý Kiến thức Thích ứng:

Đối với kết quả tìm kiếm web: Tinh chỉnh kiến thức để trích xuất các điểm chính.

Đối với các trường hợp không rõ ràng: Kết hợp nội dung tài liệu thô với kết quả tìm kiếm web đã được tinh chỉnh.

5. Tạo Phản hồi:

Sử dụng mô hình ngôn ngữ để tạo ra phản hồi giống như con người dựa trên truy vấn và kiến thức đã thu thập.

Bao gồm thông tin nguồn trong phản hồi để đảm bảo tính minh bạch.

# RAPTOR: Recursive Abstractive Processing and Thematic Organization for Retrieval

RAPTOR là một hệ thống truy xuất thông tin và hỏi-đáp tiên tiến, kết hợp tóm tắt tài liệu theo thứ bậc, truy xuất dựa trên nhúng (embedding), và tạo câu trả lời theo ngữ cảnh. Mục tiêu của nó là xử lý hiệu quả các bộ sưu tập tài liệu lớn bằng cách tạo ra một cây tóm tắt nhiều cấp độ, cho phép truy xuất thông tin cả ở mức tổng quát và chi tiết.

![alt text](image_2.png)

## Xây dựng Cây (Tree Building):
1. Bắt đầu với các tài liệu gốc ở cấp độ 0.
2. Với mỗi cấp độ:
    * Nhúng văn bản bằng cách sử dụng mô hình ngôn ngữ.
    * Phân cụm các nhúng (ví dụ: sử dụng Gaussian Mixture Models).
    * Tạo tóm tắt cho mỗi cụm.
    * Sử dụng các tóm tắt này làm văn bản cho cấp độ tiếp theo.
3. Tiếp tục cho đến khi đạt được một tóm tắt duy nhất hoặc đạt cấp độ tối đa.

## Nhúng và Truy xuất (Embedding and Retrieval):

1. Nhúng tất cả tài liệu và tóm tắt từ mọi cấp độ của cây.
2. Lưu trữ các nhúng này vào một cơ sở dữ liệu vector (ví dụ: FAISS) để tìm kiếm tương tự hiệu quả.
3. Với một truy vấn:
    * Nhúng truy vấn.
    * Truy xuất các tài liệu/tóm tắt giống nhất từ cơ sở dữ liệu vector.

## Nén theo Ngữ cảnh (Contextual Compression):
1. Lấy các tài liệu/tóm tắt đã truy xuất.
2. Sử dụng mô hình ngôn ngữ để trích xuất các phần liên quan nhất cho truy vấn.

## Tạo Câu trả lời (Answer Generation):
1. Kết hợp các phần liên quan thành một ngữ cảnh.
2. Sử dụng mô hình ngôn ngữ để tạo câu trả lời dựa trên ngữ cảnh này và truy vấn gốc.


# GraphRAG: Graph-Enhanced Retrieval-Augmented Generation







