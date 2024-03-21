from langchain_community.utilities import SQLDatabase

def load_sqlitedb(filepath=":memory:"):
    #filepath=R"C:\Users\eno.udonkwo\Desktop\2024 works\data\PVTRMS-mod.db"
    filepath=R"C:\Users\eno.udonkwo\Desktop\2024 works\data\misc.db"
    path=f"sqlite:///{filepath}"
    sqldb=SQLDatabase.from_uri(path)
    dbtablenames=sqldb.get_usable_table_names()
    context=sqldb.get_context()
    return (sqldb,dbtablenames,context)

if __name__=="__main__":
    res=load_sqlitedb()
    for name in res[2]:
        print((name,":",res[2][name]))


