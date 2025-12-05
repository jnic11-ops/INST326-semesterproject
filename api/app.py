# api/app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from system.system_controller import SystemController

# Create a single SystemController instance for the application (singleton)
_system_controller: Optional[SystemController] = None

def get_system_controller() -> SystemController:
    global _system_controller
    if _system_controller is None:
        # Optionally pass a portfolio CSV path here, or None
        _system_controller = SystemController(portfolio_csv_path=None)
    return _system_controller

app = FastAPI(title="Stock Info Analysis API", version="1.0")

class TimeRange(BaseModel):
    ticker: str
    start: str
    end: str

class NewsRequest(BaseModel):
    ticker: str
    feed_urls: List[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/stock/timeseries")
def stock_timeseries(payload: TimeRange, controller: SystemController = Depends(get_system_controller)):
    result = controller.get_stock_timeseries(payload.ticker, payload.start, payload.end)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/news/sentiment")
def news_sentiment(req: NewsRequest, controller: SystemController = Depends(get_system_controller)):
    return controller.get_news_with_sentiment(req.ticker, req.feed_urls)

@app.get("/portfolio/value")
def portfolio_value(start: str, end: str, controller: SystemController = Depends(get_system_controller)):
    try:
        val = controller.compute_portfolio_value(start, end)
        return {"total_value": val}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/portfolio/dashboard")
def portfolio_dashboard(controller: SystemController = Depends(get_system_controller)):
    try:
        return controller.build_portfolio_dashboard()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Entrypoint for running the API directly via `python -m api.app`
if __name__ == "__main__":
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)
