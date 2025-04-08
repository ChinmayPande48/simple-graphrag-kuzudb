import pandas as pd
import numpy as np
import warnings

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

def preprocess_data(df):
    
    pg_rows = df[df['Released_Year'] == 'PG'].index
    df.drop(pg_rows, inplace=True)

    df['Genre']=df['Genre'].str.split(',')
    df['Runtime']=df['Runtime'].str.replace('min',' ')

    df.drop(columns=['Meta_score'],inplace=True)
    df.drop(index=87,inplace=True)

    df['Certificate'].fillna( method ='ffill', inplace = True)
    
    df['Gross'] = df['Gross'].astype(str).str.replace(',', '')
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce').astype('Int64')
    #mean_value = df['Gross'].mean(numeric_only=True)
    df['Gross'].fillna(method='ffill', inplace=True)

    df['Series_Title'] = df['Series_Title'].str.strip()
    df['Series_Title'] = df['Series_Title'].str.lower()

    df['Director'] = df['Director'].str.strip()
    df['Director'] = df['Director'].str.lower()

    df['Star1'] = df['Star1'].str.strip()
    df['Star1'] = df['Star1'].str.lower()

    df['Star2'] = df['Star2'].str.strip()
    df['Star2'] = df['Star2'].str.lower()

    df['Star3'] = df['Star3'].str.strip()
    df['Star3'] = df['Star3'].str.lower()

    df['Star4'] = df['Star4'].str.strip()
    df['Star4'] = df['Star4'].str.lower()

    return df

def define_node_df(df):
    df_movie = df[['Series_Title',	'Released_Year',	'Certificate',	'Runtime','IMDB_Rating','Overview',	'No_of_Votes', 'Poster_Link', 'Gross']]
    df_directors = df[['Director']]
    #df_stars = df[['Star1','Star2','Star3','Star4']]
    #df_genre = df[['Genre']]
    df_star1 = df[['Star1']]
    df_star2 = df[['Star2']]
    df_star3 = df[['Star3']]
    df_star4 = df[['Star4']]

    df_movie.loc[:, 'Series_Title'] = df_movie['Series_Title'].drop_duplicates()
    df_directors.loc[:, 'Director'] = df_directors['Director'].drop_duplicates()
    #df_genre.loc[:, 'Genre'] = df_genre['Genre'].drop_duplicates()
    df_star1.loc[:, 'Star1'] = df_star1['Star1'].drop_duplicates()
    df_star2.loc[:, 'Star2'] = df_star2['Star2'].drop_duplicates()
    df_star3.loc[:, 'Star3'] = df_star3['Star3'].drop_duplicates()
    df_star4.loc[:, 'Star4'] = df_star4['Star4'].drop_duplicates()

    df_directors= df_directors.dropna()
    df_movie = df_movie.dropna()
    #df_genre= df_genre.dropna()
    df_star1= df_star1.dropna()
    df_star2= df_star2.dropna()
    df_star3= df_star3.dropna()
    df_star4= df_star4.dropna()

    df_movie['IMDB_Rating'] = pd.to_numeric(df_movie['IMDB_Rating'], errors='coerce',)
    #df_movie['Gross'] = pd.to_numeric(df_movie['Gross'], errors='coerce').astype('Int64')  # or 'Float64
    df_movie['Runtime'] = pd.to_numeric(df_movie['Runtime'], errors='coerce').astype('Int64') # or 'Float64'
    df_movie['Released_Year'] = pd.to_numeric(df_movie['Released_Year'], errors='coerce').astype('Int64')

    df_movie = df_movie.astype({
    #"MovieID": int,
    "Runtime": int,
    "Released_Year": int,
    "No_of_Votes": int,
    "Gross": int,
    "IMDB_Rating": float
    })
    

    return df_directors,df_movie,df_star1,df_star2,df_star3,df_star4

def define_rel_df(df):
    df_directed_by = df[['Series_Title','Director']]
    #df_belong_to = df[['Series_Title','Genre']]
    df_starred_in = df[['Star1','Series_Title']]
    df_second_lead_in = df[['Star2','Series_Title']]
    df_supporting_actor_in = df[['Star3','Series_Title']]
    df_second_supporting_actor_in = df[['Star4','Series_Title']]

    return df_directed_by,df_starred_in,df_second_lead_in,df_supporting_actor_in,df_second_supporting_actor_in
