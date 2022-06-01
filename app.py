from fastapi import FastAPI
from initialize_sp100 import market_status_to_dict, get_sp500_data, optimize_api_request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-entries/{strategy_name}")
def get_entries(strategy_name: str):
    if strategy_name == "full-market":
        return optimize_api_request()
    elif strategy_name == "sp500":
        return get_sp500_data()
