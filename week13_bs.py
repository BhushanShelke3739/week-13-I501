import matplotlib.pyplot as plt
import pandas as pd
import os
import streamlit as st
import seaborn as sns
#from dotenv import load_dotenv
#from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
#REMOTE_DATA = 'data_subset.csv'

#load_dotenv()

# load Backblaze connection
#b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        #key_id=os.environ['B2_KEYID'],
        #secret_key=os.environ['B2_APPKEY'])

df_new = pd.read_csv("C:/Users/bhush/Downloads/Coursework/INFO I 501/project/data_subset.csv")

#b2.set_bucket(os.environ['B2_BUCKETNAME'])

#df_new = b2.to_df(REMOTE_DATA)
# Drop rows with null values
df_new = df_new.dropna()


# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
st.write(
'''
## TMDB movie dataset
This dataset is loaded from my local computer, and rendered in Streamlit using `st.dataframe()`.
This is a subset of the original TMDB dataset.
''')


st.dataframe(df_new)

# ------------------------------
# PART 1 : Filter Data
# ------------------------------

tmp = df_new.groupby("release_year").agg({"revenue":"mean"})
tmp = tmp[tmp['revenue']!=0].reset_index()

# ------------------------------
# PART 2 : Plot
# ------------------------------

st.write(
'''
### Data viz. using Matplotlib
Finding out average revenue over the years
'''
)
sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 6))

plt.bar(x=tmp["release_year"], height=tmp["revenue"], color='skyblue')


plt.xlabel('Release Year', fontsize=14, labelpad=10)
plt.ylabel('Revenue in Billions', fontsize=14, labelpad=10)
plt.title('Movie Revenue Over the Years', fontsize=18, pad=20)

ax.yaxis.grid(True, linestyle='--', alpha=0.7)

plt.show()

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)

# ------------------------------
# PART 3 : Plot 2
# ------------------------------

tmp1 = df_new.groupby("production_companies").agg({"revenue":"mean"})
tmp1 = tmp1[tmp1['revenue']!=0].reset_index()
tmp1 = tmp1.sort_values(by='revenue', ascending=False)
tmp1 = tmp1.head(10)


st.write(
'''
### Data viz. using Matplotlib - 2
Finding out the top 10 succesful production companies.
'''
)

sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(10, 9))

plt.barh(tmp1["production_companies"], tmp1["revenue"], color='skyblue')

plt.xlabel('Mean Revenue in Billions', fontsize=14, labelpad=10)
plt.ylabel('Production Companies', fontsize=14, labelpad=10)
plt.title('Top 10 Successful Production Companies in the Past Few Years', fontsize=18, pad=20)

plt.gca().invert_yaxis()

plt.show()

st.pyplot(fig)

st.markdown(
    '''
    ### Mapping and Filtering Our Data
    We will use a slider to find the fans' favorite movie of the year.
    '''
)

# Slider for selecting the release year
year_selected = st.selectbox("Release year: ",[2015,2016,2017,2018,2019,2020,2021,2022,2023])

# Filter movies released before the selected year
movies_in_year = df_new[df_new['release_year'] == year_selected]

# Find the movie with the highest vote average
max_vote_movie = movies_in_year.loc[movies_in_year['vote_average'].idxmax()]

# Display the result using st.write
st.title(max_vote_movie['title'])
# ------------------------------
