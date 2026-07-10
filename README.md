# VietinBank · Hệ thống Quản trị Rủi ro Hoạt động (app1.py)

Ứng dụng Streamlit minh họa mô hình **Ba vòng kiểm soát (Three Lines of Defense)** trong quản trị Rủi ro Hoạt động (RRHĐ), mô phỏng cách VietinBank vận hành quy trình nhận diện — đo lường — kiểm soát — giám sát — báo cáo rủi ro.

## Cấu trúc file

### 1. Cấu hình & giao diện thương hiệu (dòng 1–140)
- Thiết lập trang (`st.set_page_config`) với tiêu đề, icon, layout rộng.
- Bảng màu theo bộ nhận diện VietinBank: xanh dương (`#0055A5`), xanh đậm (`#00336B`), đỏ (`#E31E24`).
- Thang màu riêng cho ma trận nhiệt (`CTG_HEATSCALE`): từ cam nhạt (an toàn) đến đỏ (nguy hiểm).
- Hàm `inject_css()`: tùy biến giao diện Streamlit mặc định — header, sidebar, thẻ chỉ số (metric), nút bấm, tab, form — theo phong cách nhận diện ngân hàng.
- Hàm `render_header()`: vẽ thanh tiêu đề có logo VietinBank ở đầu mỗi trang.
- Hàm `brand_layout()`: áp font chữ, màu nền, lưới cho các biểu đồ Plotly.

### 2. Danh mục dữ liệu nghiệp vụ (dòng 143–162)
- `ERRORS_POOL`: 6 loại lỗi tác nghiệp mẫu (giao dịch vượt thẩm quyền, lệch sổ sách kế toán, nhận diện sai khách hàng, sự cố IT, gian lận nội bộ, thiếu nhân sự quản lý).
- `RISK_TYPES`: 6 loại rủi ro trọng yếu tương ứng.
- `ERROR_TO_RISK_MAP`: ánh xạ mỗi lỗi cụ thể sang đúng loại rủi ro trọng yếu — mô phỏng cách phân loại sự kiện theo chuẩn Basel.
- `BRANCHES`: danh sách 4 chi nhánh mẫu (TP.HCM, Hà Nội, Đà Nẵng, Cần Thơ).

### 3. Cơ sở dữ liệu giả lập (dòng 165–195)
- Dùng `st.session_state` để lưu trữ tạm trong phiên làm việc — đóng vai trò như một "kho dữ liệu tổn thất" (loss database) thu nhỏ.
- Khởi tạo sẵn một số sự kiện lỗi mẫu và dữ liệu KRI theo tháng (số phàn nàn khách hàng) để dashboard có dữ liệu hiển thị ngay khi mở app.

### 4. Điều hướng (sidebar, dòng 196–207)
- Menu radio cho phép chuyển giữa 3 phân hệ, tương ứng với 3 vòng kiểm soát của VietinBank.

### 5. Vòng 1 — Khối Tác nghiệp / Chi nhánh (dòng 211–253)
Mô phỏng **người sở hữu rủi ro** trực tiếp nhận diện & kiểm soát:
- Form nhập liệu: chọn chi nhánh, chọn lỗi tác nghiệp, đánh giá định tính theo thang 1–5 cho "khả năng xảy ra" và "mức độ ảnh hưởng" — chính là bước RCSA sơ bộ.
- Khi bấm nút ghi nhận: hệ thống tự sinh mã sự kiện (`SKRRHĐ-1000`, `SKRRHĐ-1001`...), gắn ngày phát hiện, trạng thái mặc định "Chưa khắc phục", rồi thêm vào bảng dữ liệu chung.
- Bảng hiển thị bên phải: danh sách 10 sự kiện gần nhất, tô màu theo trạng thái (đỏ nhạt = chưa khắc phục, xanh nhạt = đã khắc phục) để dễ theo dõi trực quan.

### 6. Vòng 2 — Phòng Quản lý RRHĐ (dòng 258–327)
Mô phỏng vai trò **giám sát độc lập** với 2 công cụ đo lường:
- **3 chỉ số tổng quan**: tổng số lỗi, số lỗi đã khắc phục, tỷ lệ khắc phục kịp thời — tính động từ dữ liệu Vòng 1.
- **Tab "Ma trận định tính RCSA"**: dựng ma trận nhiệt 5×5 (Plotly heatmap) đếm số lượng sự kiện rơi vào từng ô khả năng × ảnh hưởng — trực quan hóa việc "chốt rủi ro trọng yếu".
- **Tab "Chỉ số định lượng KRI"**: biểu đồ đường thể hiện xu hướng số phàn nàn khách hàng qua các tháng, kèm 2 đường ngưỡng cố định (ngưỡng chấp nhận ≤40, ngưỡng nguy hiểm ≥60). Có logic cảnh báo tự động (`st.error` / `st.warning` / `st.success`) tùy theo giá trị tháng gần nhất so với ngưỡng.

### 7. Vòng 3 — Kiểm toán Nội bộ (dòng 332–361)
Mô phỏng vai trò **đánh giá độc lập toàn hệ thống**:
- Bộ lọc theo chi nhánh và trạng thái xử lý, hiển thị số bản ghi khớp điều kiện.
- Nút xuất báo cáo CSV (mã hóa UTF-8-sig để hiển thị tiếng Việt đúng khi mở bằng Excel).
- Khối khuyến nghị cố định, thể hiện quan điểm kiểm toán: đề xuất đổi cách tính KPI từ "lỗi trọng yếu" sang "tổng số lỗi ròng", và đề xuất tích lũy dữ liệu tổn thất 3–5 năm để chuẩn bị cho mô hình định lượng nâng cao (AMA/SA).

## Logic xuyên suốt

Toàn bộ 3 phân hệ dùng **chung một nguồn dữ liệu** (`st.session_state.operational_events`) — sự kiện được Vòng 1 nhập vào sẽ ngay lập tức xuất hiện trong dashboard Vòng 2 và bộ lọc Vòng 3. Cách thiết kế này minh họa đúng nguyên tắc của mô hình 3 vòng kiểm soát: dữ liệu chảy xuyên suốt từ nơi phát sinh rủi ro đến nơi giám sát và kiểm toán, không tách rời thành các hệ thống rời rạc.
