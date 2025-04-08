import kuzu
import shutil

db = kuzu.Database("imdb")
conn = kuzu.Connection(db)


def drop_rel():
    conn.execute("DROP TABLE DIRECTED_BY;")
    #conn.execute("DROP TABLE BELONG_TO;")
    conn.execute("DROP TABLE STARRED_IN;")
    conn.execute("DROP TABLE SECOND_LEAD_IN;")
    conn.execute("DROP TABLE SUPPORTING_ACTOR_IN;")
    conn.execute("DROP TABLE SECOND_SUPPORTING_ACTOR_IN;")

def drop_node():
    conn.execute("DROP TABLE Movie;")
    conn.execute("DROP TABLE Director;")
    #conn.execute("DROP TABLE Genre;")
    conn.execute("DROP TABLE Star1;")
    conn.execute("DROP TABLE Star2;")
    conn.execute("DROP TABLE Star3;")
    conn.execute("DROP TABLE Star4;")

def create_node():
    conn.execute("CREATE NODE TABLE Movie(Series_Title STRING, Released_Year INT64, Certificate STRING, Runtime INT64, IMDB_Rating FLOAT4, Overview STRING, No_of_Votes INT64, Poster_Link STRING,Gross INT64, PRIMARY KEY(Series_Title));")
    conn.execute("CREATE NODE TABLE Director(Director STRING, PRIMARY KEY(Director));")
    conn.execute("CREATE NODE TABLE Star1(Star1 STRING, PRIMARY KEY(Star1));")
    conn.execute("CREATE NODE TABLE Star2(Star2 STRING, PRIMARY KEY(Star2));")
    conn.execute("CREATE NODE TABLE Star3(Star3 STRING, PRIMARY KEY(Star3));")
    conn.execute("CREATE NODE TABLE Star4(Star4 STRING, PRIMARY KEY(Star4));")
def ingest_node_data():
    conn.execute("COPY Movie FROM df_movie (ignore_errors=true);")
    conn.execute("COPY Director from df_directors (ignore_errors=true);")
    #conn.execute("COPY Genre from df_genre (ignore_errors=true);")
    conn.execute("COPY Star1 from df_star1 (ignore_errors=true);")
    conn.execute("COPY Star2 from df_star2 (ignore_errors=true);")
    conn.execute("COPY Star3 from df_star3 (ignore_errors=true);")
    conn.execute("COPY Star4 from df_star4 (ignore_errors=true);")
def create_rel():
    conn.execute("CREATE REL TABLE DIRECTED_BY(FROM Movie TO Director);")
    #conn.execute("CREATE REL TABLE BELONG_TO(FROM Movie TO Genre);")
    conn.execute("CREATE REL TABLE STARRED_IN(FROM Star1 TO Movie);")
    conn.execute("CREATE REL TABLE SECOND_LEAD_IN(FROM Star2 TO Movie);")
    conn.execute("CREATE REL TABLE SUPPORTING_ACTOR_IN(FROM Star3 TO Movie);")
    conn.execute("CREATE REL TABLE SECOND_SUPPORTING_ACTOR_IN(FROM Star4 TO Movie);");
    
def ingest_rel_data():
    conn.execute("COPY DIRECTED_BY from df_directed_by (ignore_errors=true)")
    conn.execute("COPY STARRED_IN from df_starred_in (ignore_errors=true)")
    conn.execute("COPY SECOND_LEAD_IN from df_second_lead_in (ignore_errors=true)")
    conn.execute("COPY SUPPORTING_ACTOR_IN from df_supporting_actor_in (ignore_errors=true)")
    conn.execute("COPY SECOND_SUPPORTING_ACTOR_IN from df_second_supporting_actor_in (ignore_errors=true)")
