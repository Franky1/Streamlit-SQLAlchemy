import streamlit as st

from utils import database  # changed from database to database2

# set basic page config
st.set_page_config(page_title="Streamlit SQLAlchemy ORM",
                    page_icon=':dvd:',
                    layout='wide',
                    initial_sidebar_state='expanded')

# apply custom css if needed
# with open('assets/styles/style.css') as css:
#     st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


@st.cache_resource(ttl=3600, show_spinner=False)
def get_database_session():
    return database.get_database_session()


@st.cache_resource(show_spinner=False)
def build_streamlit_header() -> None:
    st.title(':dvd: Streamlit SQLAlchemy 2.0 ORM Example :dvd:')
    st.markdown("""
        This app is only a simple example of how to use SQLAlchemy 2 with Streamlit.
        """)
    # st.write("---")


@st.cache_data(show_spinner=False, hash_funcs={database.Post: lambda post: post.uuid})
def get_image_from_post(post: database.Post) -> bytes:
    return post.avatar


# TODO: cache doesn't work with this function
# @st.cache_data(show_spinner=False, experimental_allow_widgets=True, hash_funcs={database.Post: lambda post: post.uuid})
def build_streamlit_post(post: database.Post) -> None:
    posts_container = st.container()
    posts_columns = posts_container.columns([1, 11], gap="large")
    posts_columns[0].image(get_image_from_post(post), output_format='PNG')
    posts_columns[1].subheader(body=post.title, divider=True)
    posts_columns[1].write(post.content)
    posts_columns[1].text(f"Author: {post.author}")
    posts_columns[1].text(f"Created: {post.created}  |  ID: {post.id}  |  UUID: {post.uuid}")
    posts_container.write("---")


if __name__ == "__main__":
    if 'db' not in st.session_state:
        session_ = database.get_database_session()
        st.session_state.db = session_
    build_streamlit_header()

    st.header(body="Actions", divider=True)
    st.write("<br>", unsafe_allow_html=True)
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
    st.write("<br>", unsafe_allow_html=True)

    st.header(body="Posts", divider=True)
    st.write("<br>", unsafe_allow_html=True)

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
        # get_image_from_post.clear_cache()

    posts = database.get_all_posts_sorted_desc(st.session_state.db)

    with st.container():
        for post in posts:
            build_streamlit_post(post)

    with st.sidebar:
        st.header('About')
        st.write("---")
        st.subheader('📊 Database Stats 📊')
        st.write(f"Total Posts: {database.get_post_count(st.session_state.db)}")
