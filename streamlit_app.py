# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("Customize Your Smoothie")
st.write("Choose the fruit you want in your customize smoothie")

title = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", title)

cnx = st.connection("Snowflake")
session = cnx.session()

# Get Fruit_Name + Search_On from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)
pd_df = my_dataframe.to_pandas()

# ✅ Use Pandas list for multiselect options
ingredient_list = st.multiselect(
    "Choose up to five ingredients!",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredient_list:
    # Join with comma separator
    ingredients_string = ", ".join(ingredient_list)

    for fruit_chosen in ingredient_list:
        # ✅ Lookup Search_On value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.write(f"The search value for {fruit_chosen} is {search_on}.")
        st.subheader(f"{fruit_chosen} Nutrition information")

        # ✅ Use search_on for API call
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Insert into orders table
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{title}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered!, {title}", icon="✅")
