import streamlit as st
import easyocr
import sqlite3
import cv2
import numpy as np
import pandas as pd

# Connect to sqlite3 database
conn = sqlite3.connect('card_info.db')
c = conn.cursor()

# Create a table to store the business card information
c.execute('''CREATE TABLE IF NOT EXISTS Business_card 
              (id INT AUTO_INCREMENT PRIMARY KEY,
              name TEXT,
              position TEXT,
              address TEXT,
              pincode VARCHAR(25),
              phone VARCHAR(25),
              email TEXT,
              website TEXT,
              company TEXT
              )''')

# Using easyOCR for reading data
reader = easyocr.Reader(['en'],gpu=False)

# Set the title and page icon
st.set_page_config(page_title="BIZCARD-X", page_icon="::")

# Title
st.title(":green[Business Card Data Extractor]")

# Create a file uploader
file_upload = st.file_uploader(
    ":red[Please upload an image and then choose an option from the dropdown box on the left to upload or view or edit the information on the card.]",
    type=["jpg", "jpeg", "png"])

# Create a sidebar menu with options to Add, Show, Update business card information
st.sidebar.title(":red[BIZCARD-X]")


m = ['Upload Card Info', 'View Card Info', 'Edit Card Info']
choose = st.sidebar.selectbox("Select An Option:", m)

if choose == 'Upload Card Info':
    if file_upload is not None:

        # Read the image using OpenCV
        image = cv2.imdecode(np.fromstring(file_upload.read(), np.uint8), 1)

        # Display the uploaded image
        st.image(image, caption='Uploaded Successfully', use_column_width=True)

        # Button to extract information from the image
        if st.button('Extract Data And Append'):
            bsc = reader.readtext(image, detail=0)
            text = "\n".join(bsc)

            # Insert the extracted information and image into the database
            sql_data = "INSERT INTO Business_card (name, position, address, pincode, phone, email, website, company) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (bsc[0], bsc[1], bsc[2], bsc[3], bsc[4], bsc[5], bsc[6], bsc[7])
            c.execute(sql_data, values)
            conn.commit()

            # Display message
            st.success("Card Data Inserted")

elif choose == 'View Card Info':

    # Display the stored business card information
    c.execute("SELECT * FROM Business_card")
    result = c.fetchall()
    df = pd.DataFrame(result,
                      columns=['id', 'name', 'position', 'address', 'pincode', 'phone', 'email', 'website', 'company'])
    st.balloons()
    st.write(df)


elif choose == 'Edit Card Info':

    # Create a dropdown menu to select a business card to edit
    c.execute("SELECT id, name FROM Business_card")
    result = c.fetchall()
    business_cards = {}

    for row in result:
        business_cards[row[1]] = row[0]
    select_card_name = st.selectbox("Select Card To Edit", list(business_cards.keys()))

    # Get the current information for the selected business card
    c.execute("SELECT * FROM Business_card WHERE name=?", (select_card_name,))
    result = c.fetchone()

    # Get edited information
    name = st.text_input("Name", result[1])
    position = st.text_input("Position", result[2])
    address = st.text_input("Address", result[3])
    pincode = st.text_input("Pincode", result[4])
    phone = st.text_input("Phone", result[5])
    email = st.text_input("Email", result[6])
    website = st.text_input("Website", result[7])
    company = st.text_input("Company_Name", result[8])

    # Create a button to update the business card
    if st.button("Edit Card Data"):
        # Update the information for the selected business card in the database
        c.execute(
            "UPDATE Business_card SET name=?, position=?, address=?, pincode=?, phone=?, email=?, website=?, company=? WHERE name=?",
            (name, position, address, pincode, phone, email, website, company, select_card_name))
        conn.commit()
        st.success("Card Data Updated")