# VietinBank · Hệ thống Quản trị Rủi ro Hoạt động (Demo)

Ứng dụng minh họa mô hình **Ba vòng kiểm soát (Three Lines of Defense)** trong quản trị Rủi ro Hoạt động (RRHĐ) tại VietinBank, được xây dựng bằng Streamlit cho đề tài "Quản trị Rủi ro Hoạt động — Nghiên cứu trường hợp VietinBank".

## Giới thiệu

Ứng dụng mô phỏng quy trình quản trị RRHĐ theo chuẩn ISO 31000 và định hướng Basel II, chia thành 3 phân hệ tương ứng với 3 vòng kiểm soát:

| Vòng | Vai trò | Chức năng trong app |
|---|---|---|
| **Vòng 1** | Khối Tác nghiệp (Chi nhánh) | Ghi nhận sự kiện lỗi tác nghiệp, đánh giá định tính RCSA (khả năng xảy ra × mức độ ảnh hưởng) |
| **Vòng 2** | Phòng Quản lý RRHĐ (TSC) | Dashboard giám sát độc lập: ma trận nhiệt RCSA 5×5, chỉ số KRI (số phàn nàn khách hàng) với ngưỡng cảnh báo |
| **Vòng 3** | Kiểm toán Nội bộ | Lọc, trích xuất dữ liệu tổn thất, xuất báo cáo CSV, khuyến nghị cải thiện |

## Yêu cầu hệ thống

- Python 3.9+
- Các thư viện: `streamlit`, `pandas`, `numpy`, `plotly`

## Cài đặt

```bash
pip install streamlit pandas numpy plotly
```

## Chạy ứng dụng

```bash
streamlit run app1.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`.

## Hướng dẫn sử dụng

1. **Chọn phân hệ** ở thanh điều hướng bên trái (sidebar) — tương ứng với Vòng 1, 2, hoặc 3.
2. **Vòng 1:**
   - Chọn chi nhánh, loại lỗi tác nghiệp từ danh mục có sẵn.
   - Đánh giá "Khả năng xảy ra" và "Mức độ ảnh hưởng" theo thang 1–5 (RCSA).
   - Bấm **"Ghi nhận sự kiện rủi ro"** — hệ thống tự sinh mã sự kiện (SKRRHĐ-xxxx) và lưu vào cơ sở dữ liệu phiên làm việc.
3. **Vòng 2:**
   - Xem 3 chỉ số tổng quan: tổng số lỗi, số lỗi đã khắc phục, tỷ lệ khắc phục.
   - Tab "Ma trận định tính RCSA": biểu đồ nhiệt thể hiện phân bố lỗi theo tần suất × ảnh hưởng.
   - Tab "Chỉ số định lượng KRI": biểu đồ xu hướng số phàn nàn khách hàng theo tháng, kèm cảnh báo tự động khi vượt ngưỡng (≤40: an toàn, 40–60: cảnh báo, ≥60: nguy hiểm).
4. **Vòng 3:**
   - Lọc dữ liệu tổn thất theo chi nhánh / trạng thái xử lý.
   - Xuất báo cáo CSV.
   - Xem khuyến nghị cải thiện từ góc nhìn kiểm toán nội bộ.

## Lưu ý kỹ thuật

- Dữ liệu được lưu bằng `st.session_state`, chỉ tồn tại trong phiên làm việc hiện tại (refresh trang sẽ mất dữ liệu vừa nhập, trừ dữ liệu khởi tạo mẫu).
- Đây là **bản demo minh họa quy trình**, chưa kết nối cơ sở dữ liệu thật hay hệ thống core banking.

## Ánh xạ với khung lý thuyết

| Thành phần trong app | Khái niệm lý thuyết tương ứng |
|---|---|
| Form ghi nhận sự kiện (Vòng 1) | Bước 1 — Nhận diện rủi ro |
| Slider khả năng xảy ra / ảnh hưởng | Đánh giá định tính RCSA |
| Ma trận nhiệt 5×5 | Công cụ đo lường theo ma trận 5×5 |
| Biểu đồ KRI + ngưỡng cảnh báo | Bước 4 — Giám sát bằng chỉ số cảnh báo sớm (KRIs) |
| Bộ lọc + xuất CSV (Vòng 3) | Bước 5 — Báo cáo, phục vụ kiểm toán độc lập |

## Tác giả

Nhóm 2 — Môn Quản trị Rủi ro Ngân hàng
GV hướng dẫn: PGS. TS. Lê Hoàng Anh
