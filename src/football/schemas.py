from pydantic import BaseModel


# class SPredictionInput(BaseModel):
#     team: str
#     opponent: str
#     goals: int
#     home_advantage: bool


class SPredictionOutput(BaseModel):
    home_win_prob: float
    draw_prob: float
    away_win_prob: float


