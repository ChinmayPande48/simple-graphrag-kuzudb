from data_ingestion import load_imdb_data
from data_preprocessing import preprocess_data,define_node_df,define_rel_df
from graph_db import drop_rel,drop_node,create_node,ingest_node_data,create_rel,ingest_rel_data
from integrate_llm import graphRagQA

#load dataset
df = load_imdb_data()

#preprocess data
df = preprocess_data(df)

df_directors,df_movie,df_star1,df_star2,df_star3,df_star4 = define_node_df(df)
df_directed_by,df_starred_in,df_second_lead_in,df_supporting_actor_in,df_second_supporting_actor_in = define_rel_df(df)

#create db

#drop_rel()
#drop_node()
create_node()
ingest_node_data()
create_rel()
ingest_rel_data()

#invoke QAChain


query = input("Enter a movie question:\n")
result=graphRagQA(query)
print(result)
