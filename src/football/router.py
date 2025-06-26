from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sklearn.linear_model import LogisticRegression
from sqlalchemy import select, func, case, or_
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from football.fb_dao import TeamDAO
from football.models import Team, Match

router = APIRouter(prefix="/prediction", tags=["football"])



@router.get("/predict/{home_team}/{away_team}", response_model=dict)
async def predict(home_team: str, away_team: str):
    """
    Прогнозирует вероятность победы команды дома против соперника.
    Возвращает значение вероятности победы домашней команды.
    """
    async with db_helper.session_factory() as session:
        # Выбор статистики побед для двух указанных команд
        stmt = (
            select(Team.name.label("team_name"),
                   func.count(Match.id).label("total_matches"),
                   func.sum(case((Match.home_score > Match.away_score, 1), else_=0)).label("wins"))
            .join(Match, or_(Match.team_home_id == Team.id, Match.team_away_id == Team.id))
            .where(Team.name.in_([home_team, away_team]))
            .group_by(Team.name)
        )

        # Выполнение запроса
        result = await session.execute(stmt)
        rows = result.all()

        if len(rows) != 2:
            raise HTTPException(status_code=404, detail="Данные о командах отсутствуют или недостаточны.")

        # Преобразование результата в DataFrame
        df = pd.DataFrame(rows, columns=["team_name", "total_matches", "wins"])
        df["win_percentage"] = df["wins"] / df["total_matches"]

        # Обучаем простую модель классификации
        X_train = df[["win_percentage"]].values.reshape(-1, 1)
        y_train = [1 if row['team_name'] == home_team else 0 for _, row in df.iterrows()]
        model = LogisticRegression().fit(X_train, y_train)

        # Формируем предсказание вероятности победы домашней команды
        prediction = model.predict_proba(df.query(f'team_name == "{home_team}"')[["win_percentage"]])[0][1]

        return {"probability": float(prediction)}


