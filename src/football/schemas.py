from pydantic import BaseModel


class SPredictionInput(BaseModel):
    team: str
    opponent: str
    goals: int
    home_advantage: bool


class SPredictionOutput(BaseModel):
    match_id: int
    team: str
    opponent: str
    win_probability: float
    predicted_winner: str
