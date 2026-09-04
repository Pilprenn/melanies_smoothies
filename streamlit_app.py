import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session
from cryptography.hazmat.primitives import serialization

# ---- Connexion via clé privée ----
s = st.secrets["connections"]["snowflake"]
p_key = serialization.load_pem_private_key(s["private_key"].encode(), password=None)
pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)
session = Session.builder.configs({
    "account": s["account"], "user": s["user"], "private_key": pkb,
    "role": s["role"], "warehouse": s["warehouse"],
    "database": s["database"], "schema": s["schema"],
}).create()

# ---- App ----
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("""Choose the fruit you want in your custom smoothie !""")

name_on_order = st.text_input('Name on smoothie: ')
st.write('The name on your smoothie will be: ', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name_on_order + ' Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
