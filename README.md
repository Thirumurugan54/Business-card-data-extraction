# Business-card-data-extraction
To read the data from the business card image file, storing and modifying using streamlit application interface. 

The required softwares to install at first are python.
In python the follwing libraries needs to be installed using pip command such as Streamlit, Pandas, Easyocr, Sqlite3 and numpy.

1. Firstly the connection to the sql database 'card_info.db' is created
2. A table required for storing the business card details is created in the connected database
3. streamlit interface is designed with title, upload button and sidebar for selecting the required field
4. Using the loop function the image is read using opencv if uploaded
5. the uploaded image is parsed for text information and stored in a variable
6. These texts are stored into the sql table created
7. The stored details are fetched from the table and converted into a pd dataframe for better visualization
8. Edit tab is also provided to change the required field of entry and updated to the sql database

The supporting files are attached.
