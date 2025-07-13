import streamlit as st
import sqlite3

DATABASE_NAME = 'user_database.db'

# Function to initialize database
def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# Function to insert message into the database
def insert_message(name, email, message):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

def app():
    st.title("Contact Us")

    # Create a sidebar for contact information
    st.sidebar.title("Contact Information")
    st.sidebar.subheader("Contact Numbers:")
    st.sidebar.write("- Dhruv Gonnade: +91 8766511598")
    st.sidebar.write("- Gaurav Madavi: +91 9881472236")
    st.sidebar.write("- Vighnesh Durge: +91 8999577938")
    st.sidebar.write("- Chetan Parate: +91 7972597315")
        
    st.sidebar.subheader("Email:")
    st.sidebar.write("- Dhruv Gonnade: dhruvgonnade@gmail.com")
    st.sidebar.write("- Gaurav Madavi: gauravmadavi@gmail.com")
    st.sidebar.write("- Vighnesh Durge: vighneshdurge@gmail.com")
    st.sidebar.write("- Chetan Parate: chetanparate@gmail.com")

    # st.sidebar.header("GitHub Profiles:")
    # st.sidebar.write("- Chetan Parate: [GitHub Profile](https://github.com/chetanp87)")

    st.write("Feel free to reach out to us using the contact form below.")
        
    # Contact Form
    st.subheader("Contact Form:")
    st.write("You can also send us a message directly using the form below.")

    # Form inputs
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Your message")

    # Submit button
    if st.button("Send Message"):
        if not name or not email or not message:
            st.warning("Please fill out all fields.")
        else:
            insert_message(name, email, message)
            st.success("Message sent successfully!")

if __name__ == "__main__":
    app()
