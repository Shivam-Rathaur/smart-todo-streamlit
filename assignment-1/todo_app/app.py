# app.py
import streamlit as st
from datetime import date, datetime, time

# imports
from database import (
    create_table,
    add_task,
    get_all_tasks,
    update_status,
    delete_task,
    update_task
)
from ai_utils import stuck_task_analysis


## 1. page configuration
st.set_page_config(
    page_title="Smart Todo App",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

## 2. custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .app-header {
        text-align: center;
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        font-size: 1rem;
        color: #64748b;
        font-weight: 400;
    }

    .task-card-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
        border: 1px solid #f1f5f9;
        transition: all 0.2s ease;
    }
    .task-card-container:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .task-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .task-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
    }

    .meta-info {
        display: flex;
        gap: 15px;
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 8px;
        align-items: center;
    }

    .priority-1 { border-left: 5px solid #ef4444; }
    .priority-2 { border-left: 5px solid #f97316; }
    .priority-3 { border-left: 5px solid #eab308; }
    .priority-4 { border-left: 5px solid #3b82f6; }
    .priority-5 { border-left: 5px solid #22c55e; }

    .status-badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-pending { background-color: #fffbeb; color: #b45309; border: 1px solid #fcd34d; }
    .badge-completed { background-color: #f0fdf4; color: #15803d; border: 1px solid #86efac; }

    .ai-insight-box {
        background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 15px;
        margin-bottom: 10px;
        color: #1e40af;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stDateInput input, .stTimeInput input {
        border-radius: 8px !important;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #94a3b8;
        font-size: 0.875rem;
    }
    .footer a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s;
    }
    .footer a:hover {
        color: #4f46e5;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

## 3. initialisation and state
create_table()

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None
if "ai_text" not in st.session_state:
    st.session_state.ai_text = None
if "ai_for_task" not in st.session_state:
    st.session_state.ai_for_task = None
if "filter" not in st.session_state:
    st.session_state.filter = "All"
if "sort" not in st.session_state:
    st.session_state.sort = "Priority"

# Init keys for Add Task form
if "new_title" not in st.session_state:
    st.session_state.new_title = ""
if "new_desc" not in st.session_state:
    st.session_state.new_desc = ""
if "new_due_date" not in st.session_state:
    st.session_state.new_due_date = date.today()
if "new_due_time" not in st.session_state:
    st.session_state.new_due_time = time(9, 0) # Default 9:00 AM
if "new_tz" not in st.session_state:
    st.session_state.new_tz = "IST"
if "new_pr" not in st.session_state:
    st.session_state.new_pr = 3 

# helper to format combined string
def format_datetime(d_val, t_val, tz_val):
    if not d_val: return None
    # returns format: "YYYY-MM-DD HH:MM AM/PM TZ"
    t_str = t_val.strftime("%I:%M %p")
    return f"{d_val} {t_str} {tz_val}"

## helper to clean AI text
def clean_ai(text: str) -> str:
    if not text: return ""
    for ch in ["#", "*", "`"]:
        text = text.replace(ch, "")
    return text.strip()

## callback for Add Task
def handle_add_task():
    t = st.session_state.new_title
    d = st.session_state.new_desc
    d_date = st.session_state.new_due_date
    d_time = st.session_state.new_due_time
    d_tz = st.session_state.new_tz
    p = st.session_state.new_pr

    if not t.strip():
        st.toast("Task title is required!", icon="⚠️")
        return
    if not d_date:
        st.toast("Due date is required!", icon="⚠️")
        return
    
    ## Format Combine String
    final_due_str = format_datetime(d_date, d_time, d_tz)

    ## Add Task
    add_task(t.strip(), d.strip(), final_due_str, p)
    st.toast("Task added successfully!", icon="✅")
    
    ## Clear Inputs via Session State keys
    st.session_state.new_title = ""
    st.session_state.new_desc = ""
    st.session_state.new_due_date = date.today()
    st.session_state.new_due_time = time(9, 0)
    st.session_state.new_tz = "IST"
    st.session_state.new_pr = 3 
    
    ## Reset UI states
    st.session_state.ai_for_task = None
    st.session_state.edit_id = None

## 4. header section
st.markdown("""
<div class="app-header">
    <div class="app-title">⚡ Smart Todo App</div>
    <div class="app-subtitle">
        An intelligent, distraction-free productivity assistant
    </div>
</div>
""", unsafe_allow_html=True)

## 5. add task form 
with st.expander("➕ Create New Task", expanded=True):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_input("Task Title", placeholder="What needs to be done?", key="new_title")
    with c2:
        st.selectbox("Priority", [1,2,3,4,5], help="1 = High, 5 = Low", key="new_pr")
        
    st.text_area("Description (optional)", placeholder="Add details, links, or notes...", height=80, key="new_desc")
    
    # Date + Time + Timezone Row
    cd1, cd2, cd3 = st.columns([2, 1.5, 1])
    with cd1:
        st.date_input("Due Date", min_value=date.today(), key="new_due_date")
    with cd2:
        st.time_input("Time", key="new_due_time")
    with cd3:
        st.selectbox("Zone", ["IST", "GMT", "UTC", "EST", "PST", "CET"], key="new_tz")

    st.button("Add Task", use_container_width=True, type="primary", on_click=handle_add_task)

## 6. dashboard (metrics & filters)
st.markdown("<br>", unsafe_allow_html=True)

tasks = get_all_tasks()

if tasks:
    done_count = sum(1 for t in tasks if t[3] == "Completed")
    total = len(tasks)
    
    col_metrics, col_filters = st.columns([1.5, 2])
    
    with col_metrics:
        st.caption(f"**Progress:** {done_count}/{total} Completed")
        st.progress(done_count / total)
        
    with col_filters:
        f1, f2 = st.columns(2)
        with f1:
            st.selectbox("Filter", ["All", "Pending", "Completed"], key="filter", label_visibility="collapsed")
        with f2:
            st.selectbox("Sort", ["Priority", "Due Date"], key="sort", label_visibility="collapsed")
else:
    st.info("No tasks yet. Add one above to get started!")


### 7. task list
st.markdown("---")

display_tasks = tasks
if st.session_state.filter != "All":
    display_tasks = [t for t in tasks if t[3] == st.session_state.filter]

if st.session_state.sort == "Priority":
    display_tasks.sort(key=lambda x: x[5]) 
else:
    display_tasks.sort(key=lambda x: (x[4] is None, x[4]))

if not display_tasks:
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 20px;">
        All caught up! Nothing to show here.
    </div>
    """, unsafe_allow_html=True)
else:
    for t in display_tasks:
        tid, title, desc, status, due, pr, _, _ = t
        
        badge_style = "badge-completed" if status == "Completed" else "badge-pending"
        priority_style = f"priority-{pr}"
        
        ### card display 
        # Note: 'due' now contains "YYYY-MM-DD HH:MM AM/PM TZ" so it displays fully
        st.markdown(f"""
        <div class="task-card-container {priority_style}">
            <div class="task-header">
                <span class="task-title">{title}</span>
                <span class="status-badge {badge_style}">{status}</span>
            </div>
            <div style="color: #475569; font-size: 0.95rem; margin-bottom: 0.5rem; line-height: 1.5;">
                {desc if desc else "<span style='color:#cbd5e1; font-style:italic;'>No description</span>"}
            </div>
            <div class="meta-info">
                <span>🗓️ {due or "No Date"}</span>
                <span>🔥 Priority {pr}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ### action buttons 
        b1, b2, b3, b4 = st.columns([1.2, 1, 1.5, 0.8])

        with b1:
            if status == "Pending":
                if st.button("✅ Done", key=f"btn_done_{tid}", use_container_width=True):
                    update_status(tid, "Completed")
                    st.session_state.ai_for_task = None
                    st.session_state.edit_id = None
                    st.rerun()
            else:
                if st.button("↩ Undo", key=f"btn_undo_{tid}", use_container_width=True):
                    update_status(tid, "Pending")
                    st.session_state.ai_for_task = None
                    st.session_state.edit_id = None
                    st.rerun()

        with b2:
            if st.button("✏ Edit", key=f"btn_edit_{tid}", use_container_width=True):
                st.session_state.ai_for_task = None 
                st.session_state.ai_text = None
                
                if st.session_state.edit_id == tid:
                    st.session_state.edit_id = None
                else:
                    st.session_state.edit_id = tid
                st.rerun()

        with b3:
            if status == "Pending":
                if st.button("🤔 Why stuck?", key=f"btn_ai_{tid}", help="Get AI insights", use_container_width=True):
                    st.session_state.edit_id = None
                    with st.spinner("Analyzing..."):
                        try:
                            ai_res = stuck_task_analysis(title)
                            st.session_state.ai_text = clean_ai(ai_res)
                        except Exception:
                            st.session_state.ai_text = "This task may feel overwhelming. Try starting with one very small step."
                        
                        st.session_state.ai_for_task = tid
                    st.rerun()

        with b4:
            if st.button("🗑", key=f"btn_del_{tid}", use_container_width=True):
                delete_task(tid)
                st.session_state.ai_for_task = None
                st.session_state.edit_id = None
                st.rerun()

        ### dynamic sections
        
        ## a) edit Form (takes precedence)
        if st.session_state.edit_id == tid:
            with st.container():
                with st.form(key=f"edit_form_{tid}"):
                    st.markdown(f"**Editing: {title}**")
                    col_e1, col_e2 = st.columns(2)
                    new_title = col_e1.text_input("Title", value=title)
                    new_priority = col_e2.selectbox("Priority", [1,2,3,4,5], index=pr-1, key=f"sel_{tid}")
                    new_desc = st.text_area("Description", value=desc or "")
                    
                    # logic to parse existing Date/Time string
                    # Format stored is: "YYYY-MM-DD HH:MM AM/PM TZ" or "YYYY-MM-DD"
                    def_date = date.today()
                    def_time = time(9, 0)
                    def_tz = "IST"

                    if due:
                        parts = due.split(' ')
                        # try to extract Date
                        try:
                            def_date = date.fromisoformat(parts[0])
                        except: pass
                        
                        # try to extract Time (e.g., "02:30 PM")
                        if len(parts) >= 3:
                            try:
                                t_str = parts[1] + " " + parts[2]
                                parsed_time = datetime.strptime(t_str, "%I:%M %p").time()
                                def_time = parsed_time
                            except: pass
                        
                        # try to extract TZ
                        if len(parts) >= 4:
                            def_tz = parts[3]

                    # 3-column Layout for Edit
                    ce1, ce2, ce3 = st.columns([2, 1.5, 1])
                    nd_date = ce1.date_input("Due Date", value=def_date)
                    nd_time = ce2.time_input("Time", value=def_time)
                    nd_tz = ce3.selectbox("Zone", ["IST", "JST", "GMT", "UTC", "EST", "PST", "CET"], index=["IST", "JST", "GMT", "UTC", "EST", "PST", "CET"].index(def_tz) if def_tz in ["IST", "JST", "GMT", "UTC", "EST", "PST", "CET"] else 0)

                    if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                        final_due = format_datetime(nd_date, nd_time, nd_tz)
                        update_task(tid, new_title.strip(), new_desc.strip(), final_due, new_priority)
                        st.session_state.edit_id = None
                        st.toast("Task updated successfully!", icon="💾")
                        st.rerun()

        ## b) AI Insight Box (only if "not" editing)
        elif st.session_state.ai_for_task == tid:
            st.markdown(f"""
            <div class="ai-insight-box">
                <div style="display: flex; align-items: center; gap: 8px; font-weight: 600; margin-bottom: 8px;">
                    <span>🤖</span> <span>Smart Insight</span>
                </div>
                {st.session_state.ai_text}
            </div>
            """, unsafe_allow_html=True)
        
        st.write("") 


## 8. footer 
st.markdown("""
<div class="footer">
    Made with ❤️ by © <a href="https://www.linkedin.com/in/shivam-rathaur/" target="_blank">Shivam Rathaur</a> IIT Hyderabad
</div>
""", unsafe_allow_html=True)

