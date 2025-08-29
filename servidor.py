from fastapi import FastAPI
from langserve import add_routes
from app import chain_with_history

app = FastAPI(
    title="Meu Assistente de Viagens - IA",
    description="Deixe o Assistente planejar a sua viagem. Faça uma pergunta!"
)

# expor a chain como API
add_routes(app, chain_with_history, path="/assistente")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)
