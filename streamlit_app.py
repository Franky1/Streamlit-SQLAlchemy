import base64

import streamlit as st

from utils import database2 as database	 # changed from database to database2

# set basic page config
st.set_page_config(page_title="Streamlit SQLAlchemy ORM",
                    page_icon=':dvd:',
                    layout='wide',
                    initial_sidebar_state='expanded')

# apply custom css if needed
# with open('assets/styles/style.css') as css:
#     st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


@st.cache_resource(ttl=3600, show_spinner=False)
def get_database():
    return database.get_database()


@st.cache_resource(show_spinner=False, experimental_allow_widgets=True)
def build_streamlit_header():
    st.title(':dvd: Streamlit Prisma ORM Example :dvd:')
    st.markdown("""
        This app is only a simple example of how to use SQLAlchemy 2 with Streamlit.
        """, unsafe_allow_html=True)
    st.write("---")


@st.cache_data(show_spinner=False)
def get_image_from_post(_post, postid):
    b64 = _post.avatar
    if b64:
        return base64.b64decode(b64)
    return None


# @st.cache_data(show_spinner=False, experimental_allow_widgets=True)
def build_streamlit_post(_post, postid):
    posts_container = st.container()
    posts_columns = posts_container.columns([1, 14], gap="small")
    posts_columns[0].image(get_image_from_post(_post, postid), output_format='PNG')
    posts_columns[1].subheader(_post.title)
    posts_columns[1].write(_post.content)
    posts_columns[1].text(f"Author: {_post.author}")
    posts_columns[1].text(f"Created at: {_post.created_at}")
    posts_container.write("---")


if __name__ == "__main__":
    if 'db' not in st.session_state:
        db_ = database.get_database()
        database.connect(db_)
        st.session_state.db = db_
    build_streamlit_header()

    col1, col2, col3, col4, col5 = st.columns(5, gap="large")
    with col1:
        button1 = st.button(label='Generate new post', use_container_width=True)
    with col2:
        button2 = st.button(label='Delete latest post', use_container_width=True )
    with col3:
        button3 = st.button(label='Delete oldest post', use_container_width=True)
    with col4:
        button4 = st.button(label='Delete random post', use_container_width=True)
    with col5:
        button5 = st.button(label='Delete all posts', use_container_width=True)

    st.write("---")
    st.header("Posts")

    if button1:
        database.generate_fake_post(st.session_state.db)
    if button2:
        post = database.get_newest_post(st.session_state.db)
        if post:
            database.delete_post(st.session_state.db, database.get_newest_post(st.session_state.db).id)
    if button3:
        post = database.get_oldest_post(st.session_state.db)
        if post:
            database.delete_post(st.session_state.db, database.get_oldest_post(st.session_state.db).id)
    if button4:
        post = database.get_random_post(st.session_state.db)
        if post:
            database.delete_post(st.session_state.db, database.get_random_post(st.session_state.db).id)
    if button5:
        database.clear_table(st.session_state.db)

    posts = database.get_all_posts_sorted(st.session_state.db)

    with st.container():
        for post in posts:
            build_streamlit_post(post, post.id)

    with st.sidebar:
        st.header('About')
        st.write("---")
        st.subheader('📊 Database Stats 📊')
        st.write(f"Total Posts: {database.get_post_count(st.session_state.db)}")

    # database.disconnect(st.session_state.db)
