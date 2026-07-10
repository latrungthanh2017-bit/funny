import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# 0. CẤU HÌNH & BỘ NHẬN DIỆN THƯƠNG HIỆU
# ==========================================
st.set_page_config(
    page_title="VietinBank · Hệ thống Quản trị Rủi ro Hoạt động",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bảng màu VietinBank
CTG_BLUE = "#0055A5"
CTG_DARK = "#00336B"
CTG_RED = "#E31E24"
CTG_LIGHT = "#EAF2FB"

# Thang màu ma trận nhiệt theo tông thương hiệu (ít: xanh nhạt -> nhiều: đỏ)
CTG_HEATSCALE = [[0.0, "#F2F7FC"], [0.45, "#7FB3E0"], [0.75, "#F0A05A"], [1.0, CTG_RED]]


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stApp {{ font-family: 'Be Vietnam Pro', sans-serif; }}
        .stApp {{ background: #F5F8FC; }}
        .block-container {{ padding-top: 1.2rem; }}

        /* ===== Header thương hiệu ===== */
        .ctg-header {{
            background: linear-gradient(120deg, {CTG_DARK} 0%, {CTG_BLUE} 70%);
            border-radius: 16px; padding: 20px 26px; margin-bottom: 22px;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 8px 24px rgba(0,51,107,.18);
        }}
        .ctg-brand {{ display: flex; align-items: center; gap: 14px; }}
        .ctg-mark {{
            width: 42px; height: 42px; border-radius: 50%;
            background: #fff; position: relative; flex: 0 0 auto;
            box-shadow: 0 2px 8px rgba(0,0,0,.15);
        }}
        .ctg-mark::before {{
            content:''; position:absolute; inset:9px; border-radius:50%;
            background: {CTG_BLUE}; clip-path: polygon(0 0, 100% 0, 100% 55%, 0 55%);
        }}
        .ctg-mark::after {{
            content:''; position:absolute; inset:9px; border-radius:50%;
            background: {CTG_RED}; clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%);
        }}
        .ctg-word {{ color:#fff; font-weight:800; font-size:22px; letter-spacing:.3px; line-height:1; }}
        .ctg-word small {{ display:block; font-weight:400; font-size:11px; opacity:.85; margin-top:3px; letter-spacing:.2px;}}
        .ctg-title {{ color:#fff; font-weight:600; font-size:17px; text-align:right; max-width:52%; opacity:.96; }}

        /* ===== Sidebar ===== */
        section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {CTG_DARK}, {CTG_BLUE}); }}
        section[data-testid="stSidebar"] * {{ color: #EAF2FB !important; }}
        section[data-testid="stSidebar"] .ctg-sb-title {{ font-weight:700; font-size:15px; letter-spacing:.4px; }}
        section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.2); }}
        /* Radio dạng nav */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
            background: rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12);
            border-radius: 10px; padding: 10px 12px; margin-bottom: 8px; transition:.15s;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{ background: rgba(255,255,255,.16); }}
        section[data-testid="stSidebar"] div[data-testid="stInfo"] {{ background: rgba(255,255,255,.08); border:none; }}

        /* ===== Thẻ chỉ số (metric) ===== */
        div[data-testid="stMetric"], div[data-testid="metric-container"] {{
            background:#fff; border:1px solid #E3ECF7; border-left:6px solid {CTG_BLUE};
            padding:16px 18px; border-radius:14px; box-shadow:0 4px 16px rgba(0,51,107,.06);
        }}
        div[data-testid="stMetricLabel"] p {{ color:#5B6B82; font-weight:500; }}
        div[data-testid="stMetricValue"] {{ color:{CTG_DARK}; font-weight:800; }}

        /* ===== Nút bấm ===== */
        .stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {{
            background: linear-gradient(120deg, {CTG_BLUE}, {CTG_DARK}); color:#fff !important;
            border:none; border-radius:10px; font-weight:600; padding:.55rem 1.1rem;
            box-shadow:0 4px 12px rgba(0,85,165,.25); transition:.15s;
        }}
        .stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover {{
            filter:brightness(1.08); transform: translateY(-1px);
        }}

        /* ===== Tabs ===== */
        .stTabs [data-baseweb="tab-list"] {{ gap:6px; }}
        .stTabs [data-baseweb="tab"] {{ border-radius:10px 10px 0 0; padding:10px 16px; font-weight:600; }}
        .stTabs [aria-selected="true"] {{ background:{CTG_LIGHT}; color:{CTG_DARK}; box-shadow: inset 0 -3px 0 {CTG_RED}; }}

        /* ===== Form & khối nội dung ===== */
        div[data-testid="stForm"] {{ background:#fff; border:1px solid #E3ECF7; border-radius:14px; padding:18px 20px; box-shadow:0 4px 16px rgba(0,51,107,.05); }}
        h1, h2, h3 {{ color:{CTG_DARK}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(subtitle: str):
    st.markdown(
        f"""
        <div class="ctg-header">
            <div class="ctg-brand">
                <div class="ctg-mark"></div>
                <div class="ctg-word">VietinBank<small>Ngân hàng TMCP Công Thương Việt Nam</small></div>
            </div>
            <div class="ctg-title">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def brand_layout(fig, height=500):
    """Áp layout thương hiệu cho biểu đồ Plotly."""
    fig.update_layout(
        height=height,
        font=dict(family="Be Vietnam Pro, sans-serif", color=CTG_DARK),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20), title_x=0.5,
    )
    fig.update_xaxes(gridcolor="#EEF3F9")
    fig.update_yaxes(gridcolor="#EEF3F9")
    return fig


inject_css()

# ==========================================
# 1. DANH MỤC NGHIỆP VỤ
# ==========================================
ERRORS_POOL = [
    "Số lần giao dịch vượt thẩm quyền được thực hiện",
    "Số lần sổ sách kế toán không cân, hoặc cuối ngày tài khoản trung gian khác 0",
    "Số trường hợp NH nhận diện sai KH",
    "Số sự cố hệ thống công nghệ thông tin",
    "Số lần gian lận nội bộ được phát hiện",
    "Số vị trí quản lý trong ngân hàng bị trống/kiêm nhiệm",
]
RISK_TYPES = [
    "Rủi ro vượt thẩm quyền quyết định phê duyệt",
    "Rủi ro lệch sổ sách kế toán cuối ngày",
    "Rủi ro do tác nghiệp hoặc gian lận bên ngoài",
    "Rủi ro công nghệ thông tin không đáp ứng sự thông suốt",
    "Rủi ro suy giảm đạo đức của cán bộ nhân viên/ gian lận nội bộ",
    "Rủi ro nhân sự không đáp ứng đủ số lượng quản lý chủ chốt",
]
ERROR_TO_RISK_MAP = dict(zip(ERRORS_POOL, RISK_TYPES))
BRANCHES = ["Chi nhánh TP.HCM", "Chi nhánh Hà Nội", "Chi nhánh Đà Nẵng", "Chi nhánh Cần Thơ"]

# ==========================================
# 2. KHỞI TẠO CƠ SỞ DỮ LIỆU GIẢ LẬP (SESSION STATE)
# ==========================================
if "operational_events" not in st.session_state:
    np.random.seed(42)
    base_date = datetime.now() - timedelta(days=365)
    init_data = []
    for i in range(200):
        evt_date = base_date + timedelta(days=int(np.random.randint(0, 365)))
        error_name = np.random.choice(ERRORS_POOL)
        init_data.append({
            "Mã sự kiện": f"SKRRHĐ-{1000+i}",
            "Ngày phát hiện": evt_date.strftime("%Y-%m-%d"),
            "Chi nhánh": np.random.choice(BRANCHES),
            "Chi tiết lỗi tác nghiệp": error_name,
            "Loại rủi ro trọng yếu": ERROR_TO_RISK_MAP[error_name],
            "Khả năng xảy ra (1-5)": int(np.random.randint(1, 6)),
            "Mức độ ảnh hưởng (1-5)": int(np.random.randint(1, 6)),
            "Trạng thái": np.random.choice(["Đã khắc phục chỉnh sửa", "Chưa khắc phục"], p=[0.85, 0.15]),
        })
    st.session_state.operational_events = pd.DataFrame(init_data)

if "kri_complaints" not in st.session_state:
    months = [(datetime.now() - timedelta(days=30 * i)).strftime("%m/%Y") for i in range(12)][::-1]
    complaints_value = [35, 38, 32, 41, 45, 39, 48, 52, 58, 62, 65, 59]
    st.session_state.kri_complaints = pd.DataFrame({"Tháng": months, "Số phàn nàn ghi nhận": complaints_value})

# ==========================================
# 3. SIDEBAR - ĐIỀU HƯỚNG
# ==========================================
st.sidebar.markdown("<div class='ctg-sb-title'>🛡️ HỆ THỐNG QUẢN TRỊ RRHĐ</div>", unsafe_allow_html=True)
st.sidebar.caption("Mô hình Ba vòng kiểm soát (BIS) · VietinBank")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "PHÂN HỆ KIỂM SOÁT",
    [
        "Vòng 1 · Khối Tác nghiệp (Chi nhánh)",
        "Vòng 2 · Phòng Quản lý RRHĐ (TSC)",
        "Vòng 3 · Kiểm toán Nội bộ & Báo cáo",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info("💡 Ứng dụng minh hoạ trên Mô hình Ba vòng kiểm soát quốc tế (BIS) áp dụng tại VietinBank.")
# ==========================================
# VÒNG 1
# ==========================================
if menu.startswith("Vòng 1"):
    render_header("Vòng kiểm soát thứ nhất · Quản lý trực tiếp tại tuyến đầu")
    st.subheader("Đơn vị sở hữu rủi ro & thực hiện tác nghiệp giao dịch")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### Đăng ký phát hiện sự kiện lỗi")
        with st.form("input_event_form", clear_on_submit=True):
            branch = st.selectbox("Chi nhánh phát sinh lỗi", BRANCHES)
            error_selected = st.selectbox("Chi tiết lỗi tác nghiệp nhận diện", ERRORS_POOL)
            st.markdown("**Đánh giá định tính ban đầu (RCSA):**")
            likelihood = st.slider("Khả năng xảy ra lặp lại (1: Rất thấp → 5: Rất cao)", 1, 5, 3)
            impact = st.slider("Mức độ ảnh hưởng nếu xảy ra tổn thất (1: Rất thấp → 5: Rất cao)", 1, 5, 3)
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
                    "Trạng thái": "Chưa khắc phục",
                }
                st.session_state.operational_events = pd.concat(
                    [pd.DataFrame([new_row]), st.session_state.operational_events], ignore_index=True
                )
                st.success(f"Đã gửi báo cáo mã {new_id} về Phòng Quản lý RRHĐ (TSC) thành công!")

    with col2:
        st.markdown("#### Danh sách sự kiện lỗi phát sinh gần nhất")
        df_display = st.session_state.operational_events.head(10)

        def highlight_status(val):
            color = "#FDE2E2" if val == "Chưa khắc phục" else "#E3F1DE"
            return f"background-color: {color}"

        st.dataframe(
            df_display.style.map(highlight_status, subset=["Trạng thái"]),
            use_container_width=True, height=450,
        )

# ==========================================
# VÒNG 2
# ==========================================
elif menu.startswith("Vòng 2"):
    render_header("Vòng kiểm soát thứ hai · Trung tâm Dashboard & Quản lý chỉ số")
    st.subheader("Đầu mối xây dựng chính sách, giám sát rủi ro độc lập từ xa")

    total_errors = len(st.session_state.operational_events)
    fixed_errors = len(
        st.session_state.operational_events[
            st.session_state.operational_events["Trạng thái"] == "Đã khắc phục chỉnh sửa"
        ]
    )
    fix_rate = (fixed_errors / total_errors) * 100 if total_errors else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng số lỗi tác nghiệp ghi nhận", f"{total_errors:,} lỗi")
    m2.metric("Số lỗi đã khắc phục kịp thời", f"{fixed_errors:,} lỗi")
    m3.metric("Tỷ lệ khắc phục ngay trong kỳ", f"{fix_rate:.1f}%",
              help="Mục tiêu duy trì tỷ lệ khắc phục ổn định của VietinBank")

    st.markdown("---")
    tab1, tab2 = st.tabs(["🔥 Ma trận định tính RCSA", "📈 Chỉ số định lượng KRI (Phàn nàn KH)"])

    with tab1:
        st.markdown("### Ma trận nhiệt phân tích rủi ro nội tại (RCSA 5×5)")
        st.write("Phân tích tương quan giữa Khả năng xảy ra và Mức độ ảnh hưởng để định vị các lỗi trọng yếu cần chốt kiểm soát.")
        matrix_data = np.zeros((5, 5))
        for _, row in st.session_state.operational_events.iterrows():
            matrix_data[row["Khả năng xảy ra (1-5)"] - 1][row["Mức độ ảnh hưởng (1-5)"] - 1] += 1
        fig_rcsa = px.imshow(
            matrix_data,
            labels=dict(x="Mức độ ảnh hưởng (Thiệt hại)", y="Khả năng xảy ra (Tần suất)", color="Số lượng lỗi"),
            x=["1-Rất thấp", "2-Thấp", "3-Trung bình", "4-Cao", "5-Rất cao"],
            y=["1-Rất thấp", "2-Thấp", "3-Trung bình", "4-Cao", "5-Rất cao"],
            color_continuous_scale=CTG_HEATSCALE, text_auto=True,
        )
        fig_rcsa.update_layout(title="Phân bố sự kiện rủi ro theo ma trận 5×5")
        st.plotly_chart(brand_layout(fig_rcsa), use_container_width=True)

    with tab2:
        st.markdown("### Giám sát chỉ số KRI: Số lượng phàn nàn của khách hàng")
        st.write("Chỉ số định lượng theo dõi định kỳ nhằm phát hiện sớm nguy cơ suy giảm chất lượng vận hành hoặc dấu hiệu vượt khẩu vị rủi ro.")
        df_kri = st.session_state.kri_complaints
        fig_kri = go.Figure()
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=df_kri["Số phàn nàn ghi nhận"],
            mode="lines+markers+text", name="Giá trị KRI thực tế",
            line=dict(color=CTG_BLUE, width=3), marker=dict(size=8, color=CTG_DARK),
            text=df_kri["Số phàn nàn ghi nhận"], textposition="top center",
        ))
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=[40] * len(df_kri), mode="lines",
            name="Ngưỡng chấp nhận (≤ 40)", line=dict(color="#2E9E5B", dash="dash"),
        ))
        fig_kri.add_trace(go.Scatter(
            x=df_kri["Tháng"], y=[60] * len(df_kri), mode="lines",
            name="Ngưỡng nguy hiểm (≥ 60)", line=dict(color=CTG_RED, width=2, dash="dot"),
        ))
        fig_kri.update_layout(
            title="Xu hướng biến động chỉ số KRI qua các tháng",
            xaxis_title="Giai đoạn đánh giá", yaxis_title="Số phàn nàn / tháng",
            yaxis=dict(range=[20, 80]), legend=dict(orientation="h", y=-0.2),
        )
        st.plotly_chart(brand_layout(fig_kri), use_container_width=True)

        latest_val = df_kri["Số phàn nàn ghi nhận"].iloc[-1]
        if latest_val >= 60:
            st.error(f"🚨 **CẢNH BÁO NGUY HIỂM:** Chỉ số tháng gần nhất đạt {latest_val} phàn nàn, chạm ngưỡng nguy hiểm! Cần kích hoạt kịch bản ứng phó khẩn cấp.")
        elif latest_val > 40:
            st.warning(f"⚠️ **CẢNH BÁO QUAN SÁT:** Chỉ số tháng hiện tại ở mức {latest_val}, đã vượt ngưỡng an toàn. Cần theo dõi sát tiến độ khắc phục.")
        else:
            st.success(f"✅ **HỆ THỐNG AN TOÀN:** Chỉ số nằm trong vùng khẩu vị rủi ro chấp nhận ({latest_val} phàn nàn).")

# ==========================================
# VÒNG 3
# ==========================================
elif menu.startswith("Vòng 3"):
    render_header("Vòng kiểm soát thứ ba · Kiểm toán độc lập & Xuất dữ liệu")
    st.subheader("Bộ phận đánh giá độc lập tính hiệu quả của toàn bộ hệ thống quản trị")

    st.markdown("### Bộ lọc trích xuất Cơ sở dữ liệu Tổn thất (Loss Database)")
    st.write("Phục vụ kiểm tra định kỳ của Ban Kiểm soát hoặc mô hình hóa kinh tế lượng nâng cao (AMA/SA).")
    df_all = st.session_state.operational_events

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_branch = st.multiselect("Lọc theo Chi nhánh", options=df_all["Chi nhánh"].unique(), default=list(df_all["Chi nhánh"].unique()))
    with col_f2:
        filter_status = st.multiselect("Lọc theo Trạng thái xử lý", options=df_all["Trạng thái"].unique(), default=list(df_all["Trạng thái"].unique()))

    df_filtered = df_all[(df_all["Chi nhánh"].isin(filter_branch)) & (df_all["Trạng thái"].isin(filter_status))]
    st.markdown(f"**Kết quả tìm kiếm:** Tìm thấy **{len(df_filtered)}** bản ghi sự kiện rủi ro.")
    st.dataframe(df_filtered, use_container_width=True)

    csv = df_filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Xuất Báo cáo Sự kiện RRHĐ (CSV)", data=csv,
        file_name=f"Bao_cao_RRHD_VietinBank_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv",
    )

    st.markdown("---")
    st.markdown("#### 📝 Khuyến nghị định hướng hoàn thiện từ Kiểm toán nội bộ")
    st.info(
        "1. **Chuyển đổi KPI tuân thủ:** kiến nghị đổi cách tính KPI từ đếm 'số lỗi trọng yếu' sang 'tổng số lỗi ròng' nhằm loại bỏ tình trạng chậm khắc phục lỗi tồn đọng tại chi nhánh.\n\n"
        "2. **Hiện đại hóa công cụ:** tích lũy dữ liệu tổn thất tối thiểu 3–5 năm liên tục để sẵn sàng cho phần mềm tính toán mô hình định lượng nâng cao, thay cho cộng gộp thủ công."
    )
