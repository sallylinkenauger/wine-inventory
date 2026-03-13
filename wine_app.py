import streamlit as st
import pandas as pd
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Wine Inventory", page_icon="🍷", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .main { background-color: #1a0a0a; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #c9a84c !important; }
    .stApp { background-color: #1a0a0a; color: #f0e6d3; }

    .metric-card {
        background: linear-gradient(135deg, #2d1515, #1a0a0a);
        border: 1px solid #c9a84c44;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-label { font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: #c9a84c; margin-bottom: 0.3rem; }
    .metric-value { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; color: #f0e6d3; line-height: 1; }

    div[data-testid="stDataFrame"] { border: 1px solid #c9a84c33; border-radius: 8px; }
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #2d1515 !important;
        color: #f0e6d3 !important;
        border: 1px solid #c9a84c66 !important;
        border-radius: 6px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #8b1a1a, #c9a84c);
        color: white;
        border: none;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.5rem 1.5rem;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.88; }
    .stSuccess { background-color: #1a2d1a !important; border-left: 3px solid #4caf50 !important; }
    .stError   { background-color: #2d1a1a !important; border-left: 3px solid #c9a84c !important; }
    .stWarning { background-color: #2d2a1a !important; border-left: 3px solid #ff9800 !important; }
    [data-testid="stSidebar"] { background-color: #120606; border-right: 1px solid #c9a84c22; }
    [data-testid="stSidebar"] label { color: #c9a84caa !important; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; }
    .divider { border: none; border-top: 1px solid #c9a84c33; margin: 1.5rem 0; }
    .stTabs [data-baseweb="tab"] { color: #c9a84caa; font-family: 'Montserrat', sans-serif; font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; }
    .stTabs [aria-selected="true"] { color: #c9a84c !important; border-bottom-color: #c9a84c !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
FILE = "wine_list.xlsx"

def load_df():
    if not os.path.exists(FILE):
        st.error(f"'{FILE}' not found. Make sure it's in the same folder as this app.")
        st.stop()
    df = pd.read_excel(FILE)
    if "Sold" not in df.columns:              df["Sold"] = 0
    if "Astrisk" not in df.columns:           df["Astrisk"] = 0
    if "Location" not in df.columns:          df["Location"] = ""
    if "Number of Bottles" not in df.columns: df["Number of Bottles"] = 0
    df["Sold"]              = df["Sold"].fillna(0).astype(int)
    df["Astrisk"]           = df["Astrisk"].fillna(0).astype(int)
    df["Number of Bottles"] = df["Number of Bottles"].fillna(0).astype(int)
    df["Remaining"]         = df["Number of Bottles"] - df["Sold"]
    return df

def save_df(df):
    df.drop(columns=["Remaining"], errors="ignore").to_excel(FILE, index=False)

def find_by_number(df, number):
    match = df[df["Number"] == int(number)]
    return match if not match.empty else None

def find_by_name(df, name):
    return df[df["Wine Name"].str.contains(name, case=False, na=False)]

def mark_sold(df, number):
    if find_by_number(df, number) is None:
        return False
    df.loc[df["Number"] == int(number), "Sold"] = 1
    save_df(df)
    return True

def get_asterisk_wines(df):
    return df[df["Astrisk"] == 1]

def next_number(df):
    return int(df["Number"].max()) + 1 if not df.empty else 1

# ── Load data ─────────────────────────────────────────────────────────────────
df = load_df()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='font-size:2.8rem; letter-spacing:0.08em;'>🍷 Wine Cellar Inventory</h1>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Summary metrics ───────────────────────────────────────────────────────────
total     = len(df)
available = len(df[df["Sold"] == 0])
sold_cnt  = len(df[df["Sold"] == 1])
notable   = len(get_asterisk_wines(df))
avg_price = df["Price"].mean() if total > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
for col, label, value in zip(
    [c1, c2, c3, c4, c5],
    ["Total Bottles", "Available", "Sold", "Notable ★", "Avg Price"],
    [total, available, sold_cnt, notable, f"${avg_price:,.0f}"]
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋  Inventory", "🔍  Search", "✅  Mark as Sold",
    "➕  Add Wine", "✏️  Edit Wine", "🗑️  Delete Wine"
])

# ── Tab 1 — Full inventory ────────────────────────────────────────────────────
with tab1:
    st.markdown("### Cellar Collection")
    col_filter, col_sort = st.columns([2, 1])
    with col_filter:
        show = st.radio("Show", ["All", "Available only", "Sold only"], horizontal=True)
    with col_sort:
        sort_by = st.selectbox("Sort by", ["Number", "Wine Name", "Vintage", "Price"])

    display = df.copy()
    if show == "Available only": display = display[display["Sold"] == 0]
    if show == "Sold only":      display = display[display["Sold"] == 1]
    display = display.sort_values(sort_by)
    st.dataframe(display, use_container_width=True, hide_index=True)

# ── Tab 2 — Search ────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Search Wines")
    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("**Search by Name**")
        name_query = st.text_input("Wine name contains...", placeholder="e.g. Château")
        if name_query:
            results = find_by_name(df, name_query)
            if results.empty:
                st.warning(f"No wines found matching '{name_query}'")
            else:
                st.success(f"{len(results)} wine(s) found")
                st.dataframe(results, use_container_width=True, hide_index=True)

    with s_col2:
        st.markdown("**Search by Number**")
        num_query = st.number_input("Wine number", min_value=1, step=1, key="search_num")
        if st.button("Look Up", key="lookup_btn"):
            result = find_by_number(df, num_query)
            if result is None:
                st.warning(f"No wine found with number {num_query}")
            else:
                st.dataframe(result, use_container_width=True, hide_index=True)

# ── Tab 3 — Mark as sold ──────────────────────────────────────────────────────
with tab3:
    st.markdown("### Mark a Bottle as Sold")
    sold_num = st.number_input("Enter wine number", min_value=1, step=1, key="sold_num")

    preview = find_by_number(df, sold_num)
    if preview is not None:
        r = preview.iloc[0]
        total_bottles = int(r["Number of Bottles"])
        total_sold    = int(r["Sold"])
        remaining     = total_bottles - total_sold

        st.markdown(f"**{r['Wine Name']}** ({r['Vintage']})")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Bottles</div><div class="metric-value">{total_bottles}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Sold</div><div class="metric-value">{total_sold}</div></div>', unsafe_allow_html=True)
        with m3:
            color = "#c0392b" if remaining == 0 else "#f0e6d3"
            st.markdown(f'<div class="metric-card"><div class="metric-label">Remaining</div><div class="metric-value" style="color:{color}">{remaining}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if remaining <= 0:
            st.error(f"No bottles remaining for wine #{sold_num} — all sold out!")
        else:
            if st.button(f"Sell 1 Bottle ({remaining} remaining)", key="mark_sold_btn"):
                idx = df[df["Number"] == int(sold_num)].index[0]
                df.at[idx, "Sold"] = total_sold + 1
                save_df(df)
                df = load_df()
                st.success(f"✓ 1 bottle sold — {remaining - 1} remaining for wine #{sold_num}!")
                st.rerun()
    else:
        st.info("Enter a wine number above to look it up.")

# ── Tab 4 — Add wine ──────────────────────────────────────────────────────────
with tab4:
    st.markdown("### Add a New Wine")
    st.markdown(f"*Next available number: **{next_number(df)}***")

    a1, a2 = st.columns(2)
    with a1:
        new_name    = st.text_input("Wine Name", placeholder="e.g. Château Margaux")
        new_vintage = st.number_input("Vintage", min_value=1900, max_value=2100, value=2020, step=1)
        new_price   = st.number_input("Price ($)", min_value=0.0, step=0.01, format="%.2f")
    with a2:
        new_location  = st.text_input("Location", placeholder="e.g. Rack A1", key="add_location")
        new_astrisk   = st.selectbox("Notable (Astrisk)", [0, 1], format_func=lambda x: "Yes ★" if x == 1 else "No", key="add_astrisk")
        new_sold      = st.number_input("Bottles Sold", min_value=0, step=1, value=0, key="add_sold")
        new_bottles   = st.number_input("Number of Bottles", min_value=0, step=1, value=0, key="add_bottles")

    if st.button("Add Wine", key="add_btn"):
        if not new_name.strip():
            st.error("Wine name cannot be empty.")
        else:
            new_row = {
                "Number":            next_number(df),
                "Wine Name":         new_name.strip(),
                "Vintage":           int(new_vintage),
                "Price":             new_price,
                "Astrisk":           new_astrisk,
                "Sold":              new_sold,
                "Location":          new_location.strip(),
                "Number of Bottles": new_bottles
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_df(df)
            st.success(f"✓ '{new_name}' added as wine #{new_row['Number']}!")
            st.rerun()

# ── Tab 5 — Edit wine ─────────────────────────────────────────────────────────
with tab5:
    st.markdown("### Edit an Existing Wine")

    edit_num = st.number_input("Enter wine number to edit", min_value=1, step=1, key="edit_num")
    edit_row = find_by_number(df, edit_num)

    if edit_row is not None:
        r = edit_row.iloc[0]
        st.markdown(f"**Editing:** {r['Wine Name']}")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        e1, e2 = st.columns(2)
        with e1:
            e_name    = st.text_input("Wine Name",   value=str(r["Wine Name"]))
            e_vintage = st.number_input("Vintage",   value=int(r["Vintage"]), min_value=1900, max_value=2100, step=1)
            e_price   = st.number_input("Price ($)", value=float(r["Price"]), min_value=0.0, step=0.01, format="%.2f")
        with e2:
            e_location = st.text_input("Location",  value=str(r["Location"]) if pd.notna(r["Location"]) else "", key="edit_location")
            e_astrisk  = st.selectbox("Notable (Astrisk)", [0, 1], index=int(r["Astrisk"]), format_func=lambda x: "Yes ★" if x == 1 else "No", key="edit_astrisk")
            e_sold     = st.number_input("Bottles Sold", min_value=0, step=1, value=int(r["Sold"]), key="edit_sold")
            e_bottles  = st.number_input("Number of Bottles", min_value=0, step=1, value=int(r["Number of Bottles"]), key="edit_bottles")

        if st.button("Save Changes", key="edit_btn"):
            idx = df[df["Number"] == int(edit_num)].index[0]
            df.at[idx, "Wine Name"]         = e_name.strip()
            df.at[idx, "Vintage"]           = int(e_vintage)
            df.at[idx, "Price"]             = e_price
            df.at[idx, "Location"]          = e_location.strip()
            df.at[idx, "Astrisk"]           = e_astrisk
            df.at[idx, "Sold"]              = e_sold
            df.at[idx, "Number of Bottles"] = e_bottles
            save_df(df)
            st.success(f"✓ Wine #{edit_num} updated successfully!")
            st.rerun()
    else:
        st.info("Enter a wine number above to load it for editing.")

# ── Tab 6 — Delete wine ───────────────────────────────────────────────────────
with tab6:
    st.markdown("### Delete a Wine")
    st.warning("⚠️ This permanently removes the wine from your list.")

    del_num = st.number_input("Enter wine number to delete", min_value=1, step=1, key="del_num")
    del_row = find_by_number(df, del_num)

    if del_row is not None:
        st.dataframe(del_row, use_container_width=True, hide_index=True)
        confirm = st.checkbox(f"Yes, I want to permanently delete wine #{del_num}")
        if confirm:
            if st.button("Delete Wine", key="del_btn"):
                df = df[df["Number"] != int(del_num)].reset_index(drop=True)
                save_df(df)
                st.success(f"✓ Wine #{del_num} deleted.")
                st.rerun()
    else:
        st.info("Enter a wine number above to load it for deletion.")
