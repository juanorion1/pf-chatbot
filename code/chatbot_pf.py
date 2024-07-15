import os
import json
import pyodbc
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
search_index = os.getenv("SEARCH_INDEX")
sql_connection = os.getenv("sql_connection")
      
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
)
      
completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "quien es el presidente de colombia?",
        },
        {
            "role": "assistant",
            "content": "Este asistente de IA no contiene información por fuera del contexto del grupo BIMBO"
        },
        {
            "role": "user",
            "content": "cuantas plantas panificadoras tiene el grupo bimbo?"
        }
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index,
                    "key": search_key,
                    "authentication": {
                        "type": "system_assigned_managed_identity"
                    }
                }
            }
        ]
    }
)

json_completion = json.loads( completion.to_json() )

content = json_completion["choices"][0]["message"]["content"]
print(content)

