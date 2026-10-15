import streamlit as st

# Page Configuration
st.set_page_config(page_title="ThriveHub", page_icon="✨", layout="centered")

# App Header
st.title("✨ ThriveHub")
st.caption("The Youth Micro-Gig & Thrift Marketplace")
st.write("Discover upcycled fashion, student services, and creative side-hustles near you.")

st.markdown("---")

# Category Filter
category = st.selectbox(
    "🔍 Filter Listings:",
    ["All Categories", "Thrift & Upcycled Fashion", "Campus Errands", "Tech & Academic Hustles"]
)

# Sample Data representing real listings
listings = [
    {
        "title": "Custom Upcycled Denim Jacket",
        "creator": "Chipo M.",
        "category": "Thrift & Upcycled Fashion",
        "price": "ZMW 180",
        "desc": "Hand-painted vintage denim jacket, size medium.",
        "whatsapp": "260970000000"
    },
    {
        "title": "Fast Python & Calculus Study Guide",
        "creator": "Lushomo",
        "category": "Tech & Academic Hustles",
        "price": "ZMW 50",
        "desc": "Clear, summarized PDF notes and practice code snippets.",
        "whatsapp": "260970000000"
    },
    {
        "title": "Dorm Move & Errands Service",
        "creator": "Kando B.",
        "category": "Campus Errands",
        "price": "ZMW 30",
        "desc": "Quick queue-standing and campus package delivery.",
        "whatsapp": "260970000000"
    }
]

# Display Listings based on filter
for item in listings:
    if category == "All Categories" or item["category"] == category:
        with st.container():
            st.subheader(item["title"])
            st.write(f"**By:** {item['creator']} | **Category:** *{item['category']}*")
            st.write(item["desc"])
            st.write(f"**Price:** {item['price']}")
            
            # Direct WhatsApp Connection Button
            wa_url = f"https://wa.me/{item['whatsapp']}?text=Hi%20{item['creator']},%20I%20saw%20your%20listing%20('{item['title']}')%20on%20ThriveHub!"
            st.link_button("📲 Connect on WhatsApp", wa_url)
            st.markdown("---")

# Footer
st.caption("Built with Python & Streamlit 🚀")
