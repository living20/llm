from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

app = FastAPI()

# Initialize the Ollama model
model = OllamaLLM(model="travelplanner")  # Adjust the model name as necessary

# Define the prompt template
template = """User: {user_message}
Assistant: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)


# Define the request and response models
class UserRequest(BaseModel):
    message: str
    user_id: str


class OllamaResponse(BaseModel):
    response: str


@app.post("/api/v1/travelplanner", response_model=OllamaResponse)
async def get_travel_plan(request: UserRequest):
    try:
        # Prepare the input for the LangChain
        chain = prompt | model
        result = chain.invoke({"user_message": request.message})

        # Print the result for debugging
        print("Model response:", result)

        # Ensure the result is a string
        if isinstance(result, str):
            return OllamaResponse(response=result)
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected response format from model: {result}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optionally, add a health check endpoint
@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
