# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")


# Write directly to the app
st.title(f" Customize Your Smoothie ")
st.write(
  "Choose the fruit you want in your customize smoothie"
)

title = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", title)
cnx = st.connection("Snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    "Choose upto five ingredients!",
    my_dataframe,
    max_selections=5
)
# Instead of manual concatenation, use join:
if ingredient_list:
    # Join with comma separator
    ingredients_string = ", ".join(ingredient_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{title}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:   # ensure only when button clicked
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered!, {title}", icon="✅")

# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json() , use_container_width= True)

    
    

    

