import streamlit as st

from library import Library
from storage_manager import StorageManager
from user import User, generate_password


def init_session():
    if "storage_manager" in st.session_state:
        return

    storage_manager = StorageManager()
    storage_manager.load_books_to_storage()
    storage_manager.load_users_to_storage()
    library = Library(storage_manager)

    if not any(user.is_admin for user in library.users.values()):
        admin = User(
            name="System",
            surname="Admin",
            username="admin",
            password="adminpassword",
            is_admin=True,
        )
        library.users[admin.username] = admin
        storage_manager.save_users()

    st.session_state.storage_manager = storage_manager
    st.session_state.library = library
    st.session_state.current_user = None


def refresh_current_user():
    current = st.session_state.current_user
    if current is None:
        return
    st.session_state.current_user = st.session_state.library.users.get(
        current.username, current
    )


def save_after_book_transaction():
    st.session_state.storage_manager.save_books()
    st.session_state.storage_manager.save_users()


def queue_success_message(message: str, tab: str):
    st.session_state.success_msg = message
    st.session_state.success_msg_tab = tab
    st.session_state.success_msg_displayed = False


def show_tab_success_message(tab: str):
    if (
        st.session_state.get("success_msg_tab") == tab
        and st.session_state.get("success_msg")
    ):
        if st.session_state.get("success_msg_displayed"):
            st.session_state.pop("success_msg", None)
            st.session_state.pop("success_msg_tab", None)
            st.session_state.pop("success_msg_displayed", None)
        else:
            st.success(st.session_state.success_msg)
            st.session_state.success_msg_displayed = True


def clear_tab_success_message(tab: str):
    if st.session_state.get("success_msg_tab") == tab:
        st.session_state.pop("success_msg", None)
        st.session_state.pop("success_msg_tab", None)
        st.session_state.pop("success_msg_displayed", None)


def show_login():
    st.title("Library System")
    st.subheader("Sign in to continue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        library = st.session_state.library
        user = library.users.get(username)
        if user and user.password == password:
            st.session_state.current_user = user
            st.rerun()
        else:
            st.error("Invalid username or password.")


def show_sidebar():
    user = st.session_state.current_user
    with st.sidebar:
        st.write(f"**{user.name} {user.surname}**")
        st.caption(f"@{user.username}")
        if user.is_admin:
            st.success("Administrator")
        else:
            st.info("Member")
        if st.button("Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()


def show_user_dashboard():
    user = st.session_state.current_user
    library = st.session_state.library

    st.title("My Library")
    tab_borrows, tab_circulation = st.tabs(["📚 My Active Borrows", "🔄 Book Circulation"])

    with tab_borrows:
        if user.borrowed_books:
            rows = [
                {"Title": title, "Copies": count}
                for title, count in sorted(user.borrowed_books.items())
            ]
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("You have no books checked out right now.")

    with tab_circulation:
        book_titles = sorted(library.db.keys())
        if not book_titles:
            st.warning("No books are available in the library yet.")
            return

        col1, col2 = st.columns(2)
        with col1:
            book_name = st.selectbox("Book", book_titles, key="user_circ_book")
            available = library.get_available_copies(book_name)
            st.caption(f"Available copies: {available}")
        with col2:
            amount = st.number_input("Number of copies", min_value=1, value=1, key="user_circ_amount")

        borrow_col, return_col = st.columns(2)
        with borrow_col:
            if st.button("Borrow", use_container_width=True, key="user_borrow"):
                success, message = library.borrow_book(user, book_name, amount)
                if success:
                    save_after_book_transaction()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        with return_col:
            if st.button("Return", use_container_width=True, key="user_return"):
                success, message = library.return_book(user, book_name, amount)
                if success:
                    save_after_book_transaction()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def show_admin_dashboard():
    library = st.session_state.library
    storage_manager = st.session_state.storage_manager

    st.title("Administration")
    tab_inventory, tab_stock, tab_users, tab_override = st.tabs(
        [
            "📊 System Inventory",
            "➕ Stock Management",
            "👤 User Management",
            "👑 Admin Override",
        ]
    )

    with tab_inventory:
        st.subheader("Books")
        if library.db:
            book_rows = [
                {
                    "Title": book.title,
                    "Author": book.author,
                    "Available Copies": book.count,
                }
                for book in library.db.values()
            ]
            st.dataframe(book_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No books in inventory.")

        st.subheader("Registered Users")
        if library.users:
            user_rows = [
                {
                    "Name": user.name,
                    "Surname": user.surname,
                    "Username": user.username,
                    "Role": "Admin" if user.is_admin else "Member",
                    "Active Borrows": user.borrowed_books or "—",
                }
                for user in sorted(library.users.values(), key=lambda u: u.username)
            ]
            st.dataframe(user_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No users registered.")

    with tab_stock:
        show_tab_success_message("stock")

        st.markdown(
            """
            <style>
            div[data-testid="stForm"]:has(input[aria-label="Copies to add"]) div[data-testid="column"] {
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            }
            div[data-testid="stForm"]:has(input[aria-label="Copies to add"])
            div[data-testid="stNumberInput"] > div,
            div[data-testid="stForm"]:has(input[aria-label="Copies to add"])
            div[data-testid="stSelectbox"] > div {
                min-height: 2.875rem;
            }
            div[data-testid="stForm"]:has(input[aria-label="Copies to add"])
            div[data-testid="stNumberInput"] input {
                min-height: 2.875rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Add New Title")
        with st.form("add_book_form"):
            new_title = st.text_input("Title")
            new_author = st.text_input("Author")
            new_count = st.number_input("Initial copies", min_value=1, value=1)
            add_submitted = st.form_submit_button("Add Book")

        if add_submitted:
            clear_tab_success_message("stock")
            if not new_title.strip():
                st.error("Title is required.")
            elif library.book_in_storage(new_title.strip()):
                st.error(f"'{new_title.strip()}' already exists. Use stock update instead.")
            else:
                library.add_new_book(new_title.strip(), new_count, new_author.strip() or None)
                storage_manager.save_books()
                queue_success_message(
                    f"Added '{new_title.strip()}' to inventory.",
                    "stock",
                )
                st.rerun()

        st.divider()
        st.markdown("#### Update Existing Stock")
        existing_titles = sorted(library.db.keys())
        if existing_titles:
            with st.form("update_stock_form"):
                stock_col1, stock_col2 = st.columns(2)
                with stock_col1:
                    selected_title = st.selectbox("Book", existing_titles)
                with stock_col2:
                    delta = st.number_input("Copies to add", min_value=1, value=1)
                update_submitted = st.form_submit_button("Update Stock")

            if update_submitted:
                clear_tab_success_message("stock")
                library.update_book_amount(selected_title, delta)
                storage_manager.save_books()
                queue_success_message(
                    f"Added {delta} copy/copies of '{selected_title}'.",
                    "stock",
                )
                st.rerun()
        else:
            st.info("Add a book first before updating stock.")

    with tab_users:
        show_tab_success_message("users")

        if st.session_state.pop("clear_create_user_password", False):
            st.session_state.create_user_password = ""

        if "create_user_password" not in st.session_state:
            st.session_state.create_user_password = ""

        if st.button("Auto-generate Password", key="auto_generate_password"):
            st.session_state.create_user_password = generate_password()
            st.rerun()

        with st.form("create_user_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            password = st.text_input(
                "Password",
                key="create_user_password",
                help="Type a password or use Auto-generate above.",
            )
            grant_admin = st.checkbox("Grant Administrator Permissions")
            create_submitted = st.form_submit_button("Create Account")

        if create_submitted:
            clear_tab_success_message("users")
            if not password.strip():
                st.error("Password is required.")
            else:
                try:
                    new_user = library.add_new_user(
                        first_name.strip(),
                        last_name.strip(),
                        is_admin=grant_admin,
                        password=password.strip(),
                    )
                    storage_manager.save_users()
                    st.session_state.clear_create_user_password = True
                    queue_success_message(
                        f"Created account **{new_user.username}** with password `{new_user.password}`.",
                        "users",
                    )
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

    with tab_override:
        normal_users = [
            user for user in library.users.values() if not user.is_admin
        ]
        book_titles = sorted(library.db.keys())

        if not normal_users:
            st.info("No member accounts available for override actions.")
            return
        if not book_titles:
            st.warning("No books in inventory.")
            return

        user_options = {user.username: user for user in normal_users}
        selected_username = st.selectbox(
            "Member",
            options=list(user_options.keys()),
            format_func=lambda u: f"{user_options[u].name} {user_options[u].surname} (@{u})",
        )
        target_user = user_options[selected_username]

        st.markdown(f"**Current borrows — {target_user.name} {target_user.surname}**")
        if target_user.borrowed_books:
            borrow_rows = [
                {"Title": title, "Copies": count}
                for title, count in sorted(target_user.borrowed_books.items())
            ]
            st.dataframe(borrow_rows, use_container_width=True, hide_index=True)
        else:
            st.info("This member has no books checked out right now.")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            book_name = st.selectbox("Book", book_titles, key="admin_override_book")
            available = library.get_available_copies(book_name)
            borrowed = target_user.borrowed_books.get(book_name, 0)
            st.caption(f"Available: {available} | Member holds: {borrowed}")
        with col2:
            amount = st.number_input("Number of copies", min_value=1, value=1, key="admin_override_amount")

        borrow_col, return_col = st.columns(2)
        with borrow_col:
            if st.button("Process Borrow", use_container_width=True, key="admin_borrow"):
                success, message = library.borrow_book(target_user, book_name, amount)
                if success:
                    save_after_book_transaction()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        with return_col:
            if st.button("Process Return", use_container_width=True, key="admin_return"):
                success, message = library.return_book(target_user, book_name, amount)
                if success:
                    save_after_book_transaction()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def main():
    st.set_page_config(page_title="Library System", page_icon="📚", layout="wide")
    init_session()
    refresh_current_user()

    if st.session_state.current_user is None:
        show_login()
        return

    show_sidebar()
    if st.session_state.current_user.is_admin:
        show_admin_dashboard()
    else:
        show_user_dashboard()


if __name__ == "__main__":
    main()
