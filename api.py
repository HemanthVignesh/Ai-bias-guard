from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from src.mitigate import mitigate_bias

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(req: AnalysisRequest):
    start_time = time.time()
    result = mitigate_bias(req.text)
    
    # Return formatted result
    return {
        "biasDetected": result.get("is_biased", False),
        "confidence": result.get("bias_score", 0.0) * 100,
        "mitigatedText": result.get("mitigated_sentence", req.text),
        "detectedGaps": [result.get("bias_type", "None")],
        "reasoning": "Analyzed locally using BART and FLAN-T5 pipeline.",
        "originalText": req.text
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
