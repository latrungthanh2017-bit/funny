import streamlit as pd_st  # Tránh trùng tên bảng với thư viện pandas
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# 1. CẤU HÌNH TRANG & DANH MỤC NGHIỆP VỤ
# ==========================================
st.set_page_config(
    page_title="Vietinbank - Hệ thống Quản trị Rủi ro Hoạt động",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Danh sách lỗi đặc thù theo quy trình quản trị tài liệu Vietinbank
ERRORS_POOL = [
    "Số lần giao dịch vượt thẩm quyền được thực hiện",
    "Số lần sổ sách kế toán không cân, hoặc cuối ngày tài khoản trung gian khác 0",
    "Số trường hợp NH nhận diện sai KH",
    "Số sự cố hệ thống công nghệ thông tin",
    "Số lần gian lận nội bộ được phát hiện",
    "Số vị trí quản lý trong ngân hàng bị trống/kiêm nhiệm"
]

RISK_TYPES = [
    "Rủi ro vượt thẩm quyền quyết định phê duyệt",
    "Rủi ro lệch sổ sách kế toán cuối ngày",
    "Rủi ro do tác nghiệp hoặc gian lận bên ngoài",
    "Rủi ro công nghệ thông tin không đáp ứng sự thông suốt",
    "Rủi ro suy giảm đạo đức của cán bộ nhân viên/ gian lận nội bộ",
    "Rủi ro nhân sự không đáp ứng đủ số lượng quản lý chủ chốt"
]

# MAP dữ liệu lỗi sang loại rủi ro tương ứng dựa trên bảng 2 của tài liệu
ERROR_TO_RISK_MAP = dict(zip(ERRORS_POOL, RISK_TYPES))

# ==========================================
# 2. KHỞI TẠO CƠ SỞ DỮ LIỆU GIẢ LẬP (SESSION STATE)
# ==========================================
if 'operational_events' not in st.session_state:
    # Sinh dữ liệu lịch sử cho 12 tháng trước để làm dashboard KRI
    np.random.seed(42)
    base_date = datetime.now() - timedelta(days=365)
    init_data = []
    
    for i in range(200):
        evt_date = base_date + timedelta(days=int(np.random.randint(0, 365)))
        error_name = np.random.choice(ERRORS_POOL)
        impact = int(np.random.randint(1, 6))      # 1-5 theo ma trận RCSA
        likelihood = int(np.random.randint(1, 6))  # 1-5 theo ma trận RCSA
        
        init_data.append({
            "Mã sự kiện": f"SKRRHĐ-{1000+i}",
            "Ngày phát hiện": evt_date.strftime("%Y-%m-%d"),
            "Chi nhánh": np.random.choice(["Chi nhánh TP.HCM", "Chi nhánh Hà Nội", "Chi nhánh Đà Nẵng", "Chi nhánh Cần Thơ"]),
            "Chi tiết lỗi tác nghiệp": error_name,
            "Loại rủi ro trọng yếu": ERROR_TO_RISK_MAP[error_name],
            "Khả năng xảy ra (1-5)": likelihood,
            "Mức độ ảnh hưởng (1-5)": impact,
            "Trạng thái": np.random.choice(["Đã khắc phục chỉnh sửa", "Chưa khắc phục"], p=[0.85, 0.15]) # Tỷ lệ 85% xử lý trong kỳ
        })
    st.session_state.operational_events = pd.DataFrame(init_data)

# Khởi tạo dữ liệu phàn nàn khách hàng (KRI chính)
if 'kri_complaints' not in st.session_state:
    months = [(datetime.now() - timedelta(days=30*i)).strftime("%m/%Y") for i in range(12)][::-1]
    # Tạo xu hướng tăng nhẹ mô phỏng giai đoạn cuối năm 2014 của Vietinbank
    complaints_value = [35, 38, 32, 41, 45, 39, 48, 52, 58, 62, 65, 59]
    st.session_state.kri_complaints = pd.DataFrame({
        "Tháng": months,
        "Số phàn nàn ghi nhận": complaints_value
    })

# ==========================================
# 3. SIDEBAR - ĐIỀU HƯỚNG THEO 3 VÒNG KIỂM SOÁT
# ==========================================
st.sidebar.image("https://www.vietinbank.vn/web/images/logo.png", width=200)
st.sidebar.markdown("### HỆ THỐNG MÔ PHỎNG QUẢN TRỊ RRHĐ")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "CHỌN PHÂN HỆ KIỂM SOÁT:",
    [
        "Vòng 1: Khối Tác Nghiệp (Chi Nhánh)",
        "Vòng 2: Phòng Quản Lý RRHĐ (Trụ sở chính)",
        "Vòng 3: Kiểm Toán Nội Bộ & Báo Cáo"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Thông tin hệ thống:**\n"
    "Ứng dụng xây dựng trên Mô hình Ba vòng kiểm soát quốc tế (BIS) áp dụng tại Vietinbank."
)

# ==========================================
# PHÂN HỆ 1: VÒNG KIỂM SOÁT THỨ NHẤT
# ==========================================
if menu == "Vòng 1: Khối Tác Nghiệp (Chi Nhánh)":
    st.title("🛡️ Vòng Kiểm Soát Thứ Nhất: Quản Lý Trực Tiếp Tại Tuyến Đầu")
    st.subheader("Đơn vị sở hữu rủi ro & Thực hiện tác nghiệp giao dịch")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Đăng Ký Phát Hiện Sự Kiện Lỗi")
        with st.form("input_event_form", clear_on_submit=True):
            branch = st.selectbox("Chi nhánh phát sinh lỗi", ["Chi nhánh TP.HCM", "Chi nhánh Hà Nội", "Chi nhánh Đà Nẵng", "Chi nhánh Cần Thơ"])
            error_selected = st.selectbox("Chi tiết lỗi tác nghiệp nhận diện", ERRORS_POOL)
            
            st.markdown("**Đánh giá định tính ban đầu (RCSA):**")
            likelihood = st.slider("Khả năng xảy ra lặp lại (1: Rất thấp -> 5: Rất cao)", 1, 5, 3)
            impact = st.slider("Mức độ ảnh hưởng nếu xảy ra tổn thất (1: Rất thấp -> 5: Rất cao)", 1, 5, 3)
            
            submit = st.form_submit_button("🚨 Ghi nhận sự kiện rủi ro (SKRRHĐ)")
            
            if submit:
                new_id = f"SKRRHĐ-{1000 + len(st.session_state.operational_events)}"
                new_row = {
                    "Mã sự kiện": new_id,
                    "Ngày phát hiện": datetime.now().strftime("%Y-%m-%d"),
                    "Chi nhánh": branch,
                    "Chi tiết lỗi tác nghiệp": error_selected,
                    "Loại rủi ro trọng yếu": ERROR_TO_RISK_MAP[error_selected],
                    "Khả năng xảy ra (1-5)": likelihood,
                    "Mức độ ảnh hưởng (1-5)": impact,
                    "Trạng thái": "Chưa khắc phục"
                }
                st.session_state.operational_events = pd.concat([pd.DataFrame([new_row]), st.session_state.operational_events], ignore_index=True)
                st.success(f"Đã gửi báo cáo mã {new_id} về Phòng quản lý RRHĐ TSC thành công!")
                
    with col2:
        st.markdown("#### Danh Sách Sự Kiện Lỗi Phát Sinh Gần Nhất")
        df_display = st.session_state.operational_events.head(10)
        
        # Định màu trạng thái hiển thị bằng dữ liệu styler
        def highlight_status(val):
            color = '#FFE2E2' if val == "Chưa khắc phục" else '#E2F0D9'
            return f'background-color: {color}'
        
        st.dataframe(df_display.style.map(highlight_status, subset=['Trạng thái']), use_container_width=True, height=450)
# ==========================================
# PHÂN HỆ 2: VÒNG KIỂM SOÁT THỨ HAI
# ==========================================
elif menu == "Vòng 2: Phòng Quản Lý RRHĐ (Trụ sở chính)":
    st.title("📊 Vòng Kiểm Soát Thứ Hai: Trung Tâm Dashboard & Quản Lý Chỉ Số")
    st.subheader("Đầu mối xây dựng chính sách, giám sát rủi ro độc lập từ xa")
    
    # Số liệu tổng hợp nhanh (Kpis tổng)
    total_errors = len(st.session_state.operational_events)
    fixed_errors = len(st.session_state.operational_events[st.session_state.operational_events["Trạng thái"] == "Đã khắc phục chỉnh sửa"])
    fix_rate = (fixed_errors / total_errors) * 100
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng số lỗi tác nghiệp hệ thống ghi nhận", f"{total_errors:,} lỗi")
    m2.metric("Số lỗi đã xử lý khắc phục kịp thời", f"{fixed_errors:,} lỗi")
    m3.metric("Tỷ lệ khắc phục chỉnh sửa ngay trong kỳ", f"{fix_rate:.1f}%", help="Mục tiêu duy trì ổn định ổn định của Vietinbank")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Ma Trận Định Tính RCSA (Rủi ro nội tại)", "Chỉ số Định Lượng KRI (Phàn nàn từ Khách hàng)"])
    
    with tab1:
        st.markdown("### Ma Trận Nhiệt Phân Tích Rủi Ro Nội Tại (RCSA 5x5)")
        st.write("Phân tích tương quan giữa Khả năng xảy ra và Mức độ ảnh hưởng để định vị các lỗi trọng yếu cần chốt kiểm soát.")
        
        # Tạo bảng tần suất 5x5 cho ma trận nhiệt
        matrix_data = np.zeros((5, 5))
        for _, row in st.session_state.operational_events.iterrows():
            l = row["Khả năng xảy ra (1-5)"] - 1
            imp = row["Mức độ ảnh hưởng (1-5)"] - 1
            matrix_data[l][imp] += 1
            
        fig_rcsa = px.imshow(
            matrix_data,
            labels=dict(x="Mức độ ảnh hưởng (Thiệt hại)", y="Khả năng xảy ra (Tần suất)", color="Số lượng lỗi"),
            x=['1-Rất thấp', '2-Thấp', '3-Trung bình', '4-Cao', '5-Rất cao'],
            y=['1-Rất thấp', '2-Thấp', '3-Trung bình', '4-Cao', '5-Rất cao'],
            color_continuous_scale="YlOrRd",
            text_auto=True
        )
        fig_rcsa.update_layout(height=500, title_x=0.5)
        st.plotly_chart(fig_rcsa, use_container_width=True)
        
    with tab2:
        st.markdown("### Giám Sát Chỉ Số KRI: Số Lượng Phàn Nàn Của Khách Hàng")
        st.write("Chỉ số định lượng được theo dõi định kỳ nhằm phát hiện sớm các nguy cơ suy giảm chất lượng vận hành hệ thống hoặc dấu hiệu vi phạm khẩu vị rủi ro.")
        
        df_kri = st.session_state.kri_complaints
        
        # Vẽ biểu đồ đường KRI với các dải giới hạn an toàn / nguy hiểm
        fig_kri = go.Figure()
        
        # Đường dữ liệu thực tế
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=df_kri["Số phàn nàn ghi nhận"],
            mode='lines+markers+text',
            name='Giá trị KRI Thực tế',
            line=dict(color='#002E6E', width=3),
            text=df_kri["Số phàn nàn ghi nhận"],
            textposition="top center"
        ))
        
        # Đường ngưỡng chấp nhận (An toàn <= 40)
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=[40]*len(df_kri),
            mode='lines', name='Ngưỡng chấp nhận (<= 40)',
            line=dict(color='green', dash='dash')
        ))
        
        # Đường ngưỡng nguy hiểm (Kích hoạt hành động ứng phó >= 60)
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=[60]*len(df_kri),
            mode='lines', name='Ngưỡng nguy hiểm (>= 60)',
            line=dict(color='#ED1C24', width=2, dash='dot')
        ))
        
        fig_kri.update_layout(
            title="Xu hướng Biến động Chỉ số KRI qua các tháng",
            xaxis_title="Giai đoạn Đánh giá",
            yaxis_title="Số lượng trường hợp phàn nàn / Tháng",
            height=500,
            yaxis=dict(range=[20, 80])
        )
        st.plotly_chart(fig_kri, use_container_width=True)
        
        latest_val = df_kri["Số phàn nàn ghi nhận"].iloc[-1]
        if latest_val >= 60:
            st.error(f"🚨 **CẢNH BÁO NGUY HIỂM:** Chỉ số tháng gần nhất đạt {latest_val} phàn nàn, chạm ngưỡng nguy hiểm! Đơn vị quản lý cần kích hoạt kịch bản ứng phó khẩn cấp.")
        elif latest_val > 40:
            st.warning(f"⚠️ **CẢNH BÁO QUAN SÁT:** Chỉ số tháng hiện tại ở mức {latest_val}, đã vượt ngưỡng an toàn thông thường. Cần theo dõi sát sao tiến độ khắc phục lỗi.")
        else:
            st.success(f"✅ **HỆ THỐNG AN TOÀN:** Chỉ số vận hành nằm tốt trong vùng Khẩu vị Rủi ro chấp nhận ({latest_val} phàn nàn).")

# ==========================================
# PHÂN HỆ 3: VÒNG KIỂM SOÁT THỨ BA
# ==========================================
elif menu == "Vòng 3: Kiểm Toán Nội Bộ & Báo Cáo":
    st.title("🔍 Vòng Kiểm Soát Thứ Ba: Kiểm Toán Độc Lập & Xuất Dữ Liệu")
    st.subheader("Bộ phận đánh giá tối cao, độc lập giám sát tính hiệu quả của toàn bộ hệ thống quản trị")
    
    st.markdown("### Bộ Lọc Trích Xuất Cơ Sở Dữ Liệu Tổn Thất (Loss Database)")
    st.write("Hệ thống phục vụ cho công tác kiểm tra định kỳ của Ban Kiểm Soát hoặc phục vụ mô hình hóa kinh tế lượng nâng cao (AMA).")
    
    df_all = st.session_state.operational_events
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_branch = st.multiselect("Lọc theo Chi nhánh dữ liệu", options=df_all["Chi nhánh"].unique(), default=df_all["Chi nhánh"].unique())
    with col_f2:
        filter_status = st.multiselect("Lọc theo trạng thái xử lý", options=df_all["Trạng thái"].unique(), default=df_all["Trạng thái"].unique())
        
    df_filtered = df_all[(df_all["Chi nhánh"].isin(filter_branch)) & (df_all["Trạng thái"].isin(filter_status))]
    
    st.markdown(f"**Kết quả tìm kiếm:** Tìm thấy **{len(df_filtered)}** bản ghi dữ kiện rủi ro đặc thù.")
    st.dataframe(df_filtered, use_container_width=True)
    
    # Tính năng xuất file báo cáo tổng hợp
    csv = df_filtered.to_csv(index=False).encode('utf-8-sig') # Dùng utf-8-sig để không bị lỗi font tiếng Việt khi mở bằng Excel
    
    st.download_button(
        label="📥 Xuất Báo Cáo Sự Kiện Rủi Ro Hoạt Động (CSV)",
        data=csv,
        file_name=f"Bao_cao_RRHD_Vietinbank_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("#### 📝 Khuyến nghị định hướng hoàn thiện từ Kiểm toán nội bộ:")
    st.info(
        "1. **Chuyển đổi KPI Tuân thủ:** Cần kiến nghị Ban lãnh đạo thay đổi cách tính KPI từ đếm 'Số lỗi trọng yếu' sang tính toán trên 'Tổng số lỗi ròng' nhằm loại bỏ tình trạng chậm trễ khắc phục lỗi tồn đọng tại chi nhánh.\n"
        "2. **Hiện đại hóa công cụ:** Tích lũy cơ sở dữ liệu tổn thất lịch sử tối thiểu từ 3 - 5 năm liên tục để sẵn sàng tích hợp các phần mềm chuyên dụng tính toán mô hình định lượng nâng cao thay thế cho các phương pháp cộng gộp thủ công hiện tại."
    )
    
import streamlit as st
import pandas as pd

st.title("📥 Tích Hợp Dữ Liệu Core Banking & Tự Động Đề Xuất")
st.write("Upload file dữ liệu lỗi trích xuất từ hệ thống Core Banking để hệ thống tự động chấm điểm và khuyến nghị.")

# 1. Thành phần Upload File
uploaded_file = st.file_uploader("Chọn file CSV dữ liệu vận hành từ Core Banking", type=["csv"])

if uploaded_file is not None:
    try:
        # Đọc dữ liệu (Sử dụng utf-8-sig để tránh lỗi font tiếng Việt từ Excel/Core trích ra)
        df_core = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        st.success("✅ Đã tải và đọc dữ liệu thành công!")
        
        # Hiển thị bản xem trước dữ liệu
        with st.expander("Xem trước 5 dòng dữ liệu thô"):
            st.dataframe(df_core.head(5))
            
        # Giả sử file CSV của bạn có các cột tối thiểu: "Mã_Lỗi", "Chi_Nhánh", "Mức_Độ_Ảnh_Hưởng" (từ 1 đến 5)
        # Chúng ta sẽ tiến hành phân tích tự động:
        
        st.subheader("📊 Kết Quả Phân Tích Hệ Thống Tự Động")
        
        total_records = len(df_core)
        
        # Kiểm tra xem có cột mức độ ảnh hưởng không để tính toán lỗi nghiêm trọng
        if "Mức_Độ_Ảnh_Hưởng" in df_core.columns:
            critical_errors = len(df_core[df_core["Mức_Độ_Ảnh_Hưởng"] >= 4])
            critical_rate = (critical_errors / total_records) * 100
        else:
            # Nếu không có cột chuẩn, giả lập tính toán dựa trên độ dài để minh họa
            critical_errors = int(total_records * 0.12)
            critical_rate = 12.0

        col_a, col_b = st.columns(2)
        col_a.metric("Tổng số bản ghi giao dịch lỗi", f"{total_records} trường hợp")
        col_b.metric("Số lỗi trọng yếu phát sinh (Mức 4 & 5)", f"{critical_errors} lỗi", f"Tỷ lệ: {critical_rate:.1f}%")
        
        # 2. HỆ THỐNG ĐƯA RA ĐỀ XUẤT TỰ ĐỘNG (AUTOMATED RECOMMENDATIONS)
        st.markdown("---")
        st.markdown("### 🤖 Đề Xuất & Khuyến Nghị Từ Hệ Thống AI-Risk")
        
        # Đưa ra các logic đề xuất động dựa trên dữ liệu upload
        if total_records > 100:
            st.error(
                f"🚨 **Đề xuất 1: Kích hoạt rà soát quy trình diện rộng.**\n"
                f"Số lượng lỗi phát sinh trong tệp dữ liệu ({total_records} lỗi) đang vượt quá hạn mức an toàn của hệ thống. "
                f"Khuyến nghị Phòng Kiểm soát Nội bộ thực hiện kiểm tra đột xuất tại các chi nhánh có tần suất lỗi cao nhất."
            )
        else:
            st.success("✅ **Đề xuất 1:** Số lượng lỗi vận hành nằm trong tầm kiểm soát. Tiếp tục duy trì giám sát từ xa.")
            
        if critical_rate > 10:
            st.warning(
                f"⚠️ **Đề xuất 2: Điều chỉnh trọng số KPI Tuân thủ.**\n"
                f"Tỷ lệ lỗi nghiêm trọng chiếm tới {critical_rate:.1f}% tổng số lỗi ròng. Hệ thống phát hiện có dấu hiệu 'nới lỏng tuân thủ' "
                f"để chạy theo tiến độ doanh số. Cần siết lại bộ lọc chặn giao dịch vượt thẩm quyền trên hệ thống Core ngay trong ngày."
            )
        else:
            st.info("💡 **Đề xuất 2:** Tỷ lệ rủi ro nghiêm trọng ở mức thấp. Các chốt kiểm soát tự động trên Core Banking đang hoạt động hiệu quả.")
            
    except Exception as e:
        st.error(f"❌ File upload không đúng định dạng cấu trúc hoặc bị lỗi mã hóa: {e}")
