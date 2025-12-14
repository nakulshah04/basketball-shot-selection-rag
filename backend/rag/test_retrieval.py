from retriever import get_retriever

retriever = get_retriever()

query = "late shot clock three pointer under tight defense"
docs = retriever.invoke(query)

for d in docs[:3]:
    print(d.page_content)