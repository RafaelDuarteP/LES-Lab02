from graphqlclient import GraphQLClient
from datetime import datetime as date
import pandas as pd
import json
import csv

url = "https://api.github.com/graphql"
token = "Bearer _token_"
today = date.utcnow()
variables = {"after": None}

query = """
query ($after: String) {
  search(query: "stars:>100 language:Java" type: REPOSITORY first: 20 after: $after) {
    pageInfo { endCursor }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        releases(first: 1, orderBy: {field: CREATED_AT, direction: ASC}) {totalCount}
        stargazerCount
      }
    }
  }


  query pullRquestsPorRepositorio {
    repository(owner: "ReactiveX", name: "RxJava") {
      pullRequests(first: 100, states: [CLOSED, MERGED]) {
        nodes {
          title
          author {
            login
          }
          state
          createdAt
          reviews {
            totalCount
          }
        }
      }
    }
  }
}
"""
client = GraphQLClient(url)
client.inject_token(token=token)

data = []

for i in range(50):
    result = json.loads(client.execute(query=query, variables=variables))
    result = result["data"]["search"]
    end_cursor = result["pageInfo"]["endCursor"]

    variables["after"] = end_cursor
    repositories = result["nodes"]

    for repo in repositories:
        created_at = date.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        data.append({
            'repository': repo['nameWithOwner'],
            'url': repo['url'],
            'age': int((today - created_at).days / 365),
            'releases': repo['releases']['totalCount'],
            'stars': repo['stargazerCount'],
            'loc': 0,
            'cbo': 0,
            'dit': 0,
            'lcom': 0,
        })

df = pd.DataFrame(data=data)

df.to_csv('dados-repo.csv', index=False)

print("fim")