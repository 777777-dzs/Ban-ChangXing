import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# ==========================================
# 页面全局配置 (已更名)
# ==========================================
st.set_page_config(page_title="伴长星 - 银发金融安全协同平台", layout="wide")

# ==========================================
# AI 调用核心引擎（带防翻车兜底机制）
# ==========================================
def call_llm(prompt, fallback_text):
    """
    调用大模型API。如果未配置API Key或请求失败，自动返回兜底文案，确保演示不翻车。
    """
    API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx" # 👉【替换这里】填入你的DeepSeek API Key
    
    if API_KEY == "sk-xxxxxxxxxxxxxxxxxxxx" or API_KEY == "":
        return fallback_text
        
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        # 设置3秒超时，防止网络卡顿影响演示
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=3)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return fallback_text

# ==========================================
# 侧边栏导航 (已更名)
# ==========================================
st.sidebar.title("🌟 伴长星")
st.sidebar.markdown("基于多方安全计算与资金风险关联图谱")
st.sidebar.caption("让科技陪伴更有温度，守护长辈资金安全")
page = st.sidebar.radio("请选择系统角色", ["👴 长辈端", "👨‍👩‍👧 亲情端", "💻 协同中心"])

st.sidebar.divider()
st.sidebar.caption("当前状态：🟢 隐私计算节点已连接")
st.sidebar.caption("版本：v2.1 Demo")

# ==========================================
# 1. 老人端 (长辈端)
# ==========================================
if page == "👴 长辈端":
    st.title("👴 伴长星 · 长辈端")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💚 养老金健康度")
        health_score = 92
        
        # 使用 Plotly 绘制半圆仪表盘
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2ecc71"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffcccc"},
                    {'range': [40, 70], 'color': "#fff3cc"},
                    {'range': [70, 100], 'color': "#ccffcc"}
                ]
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("🆘 智能紧急求助")
        st.info("遇到拿不准的事？请告诉伴长星 AI 助手，帮您分辨真假。")
        
        # 输入区
        user_input = st.text_input("对方是怎么说的？（例如：有人让我把钱转到安全账户）", 
                                   placeholder="请输入您遇到的情况...")
        
        if st.button("🚨 发送给 AI 研判", type="primary", use_container_width=True):
            if not user_input:
                st.warning("请先输入您遇到的情况。")
            else:
                with st.spinner("伴长星 AI 正在为您分析..."):
                    prompt = f"你是一个反诈助手。一位老人说：'{user_input}'。请判断他是否遇到诈骗，用50字以内给出简洁警告和防范建议。"
                    fallback = "⚠️ 危险警告：您提到的内容高度疑似“冒充公检法”或“虚假理财”诈骗！公检法绝对不会让您转账。请不要进行任何操作，您的家人和平台专员已收到通知。"
                    
                    # 调用AI
                    ai_result = call_llm(prompt, fallback)
                    time.sleep(1) # 模拟网络延迟感
                    
                    st.error(f"**伴长星 AI 研判：**\n\n{ai_result}")
                    st.success("✅ 系统已自动将风险特征推送给您的紧急联系人（子女）。")

# ==========================================
# 2. 子女端 (亲情端)
# ==========================================
elif page == "👨‍👩‍👧 亲情端":
    st.title("👨‍👩‍👧 伴长星 · 亲情端")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👤 家人信息")
        st.write("姓名：**张大爷** (父亲)")
        st.write("年龄：72岁")
        st.write("账户：尾号 8823")
        
        st.subheader("🔔 通知设置")
        st.checkbox("接收脱敏风险提示", value=True)
        st.checkbox("高风险时电话通知", value=True)
        
        st.markdown("---")
        st.subheader("👴 长辈智能关怀画像")
        st.caption("基于系统交易图谱与AI生成")
        
        if st.button("✨ 生成 AI 关怀画像", use_container_width=True):
            with st.spinner("AI 正在生成画像..."):
                prompt = "一位72岁老人，近一周发生3笔陌生账户转账，金额由200元升至5000元。请生成一份50字左右的老人风险画像，并给子女提供一段温和的劝阻话术。"
                fallback = "【画像】张大爷近期交易呈现‘试探-跟进’特征，易受保健品推销蛊惑。\n\n【建议话术】'爸，我看您晚上给XX健康转了钱，现在这种骗局很多。您先别急，等我下班回去帮您看看，咱们再决定好吗？'"
                ai_profile = call_llm(prompt, fallback)
                st.success(ai_profile)

    with col2:
        st.subheader("⚠️ 风险提示")
        
        # 模拟硬编码的预警信息
        st.warning("""
        **中风险提示**（2025-06-05 22:30）
        - **交易对手**：XX健康管理
        - **交易特征**：夜间 22:30 转账，金额 20,000 元
        - **AI 研判**：行为偏离度 82/100，匹配“保健品投资返利”骗局（匹配度 91%）
        """)
        
        st.write("**请确认是否知情：**")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ 我知情，交易正常", use_container_width=True):
                st.success("已反馈：交易正常。系统将记录该交易为正常样本，优化后续检测。")
        with col_btn2:
            if st.button("🚨 我怀疑这笔交易有问题", type="primary", use_container_width=True):
                st.error("""
                **已确认风险！系统已执行以下操作：**
                1. 伴长星冷静期自动延长至 72 小时
                2. 转平台反诈专员介入
                3. 已通知老人：您的家人对此交易有疑问，专员将与您联系
                """)
        
        st.divider()
        st.subheader("📈 家人养老金健康度趋势（14天）")
        # 模拟折线图数据
        chart_data = pd.DataFrame({
            "日期": pd.date_range(start="2025-05-23", periods=14),
            "健康度": [92, 91, 93, 90, 88, 85, 80, 75, 70, 60, 58, 55, 52, 50]
        })
        st.line_chart(chart_data.set_index("日期"), color="#ff4b4b")

# ==========================================
# 3. 管理后台 (协同中心)
# ==========================================
elif page == "💻 协同中心":
    st.title("💻 伴长星 · 协同中心")
    st.markdown("---")
    
    # 顶部指标
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("今日交易总量", "1,234 笔")
    m2.metric("低风险拦截", "45 笔", delta="+5")
    m3.metric("中风险协同", "12 笔", delta="+2", delta_color="inverse")
    m4.metric("高风险阻断", "3 笔", delta="-1", delta_color="normal")
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("⏳ 冷静期管理")
        # 模拟表格数据
        df = pd.DataFrame({
            "交易ID": ["TX1001", "TX1002"],
            "老人": ["张大爷", "李奶奶"],
            "对手方": ["XX健康管理", "XX养老公寓"],
            "金额": ["20000元", "50000元"],
            "风险等级": ["高风险", "中风险"],
            "冷静期": ["72小时", "24小时"],
            "子女确认": ["✅ 已确认风险", "⏳ 进行中"]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("📊 风险分布")
        st.bar_chart(pd.DataFrame({"风险等级": ["低风险", "中风险", "高风险"], "数量": [45, 12, 3]}).set_index("风险等级"))

    with col2:
        st.subheader("🤖 AI 智能研报助手")
        st.write("利用大模型自动总结当日风控数据，辅助平台运营决策。")
        
        if st.button("📄 一键生成今日反诈研报", type="primary", use_container_width=True):
            with st.spinner("伴长星 AI 正在汇总数据并撰写研报..."):
                prompt = "今日系统拦截低风险45笔，中风险12笔，高风险3笔。其中夜间保健品转账特征明显。请写一段100字左右的管理层反诈研报摘要。"
                fallback = """
                **今日伴长星 AI 研报摘要：**
                1. **高危特征**：今日夜间22:00-24:00出现3笔异常大额转账，均匹配“保健品投资返利”图谱节点。
                2. **协同情况**：共触发预警5次，亲情端平均响应时间12分钟，成功率80%。
                3. **AI建议**：建议明日重点向老年客户推送“夜间转账防骗”的语音提示。
                """
                report = call_llm(prompt, fallback)
                st.info(report)