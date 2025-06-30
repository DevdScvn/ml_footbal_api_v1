import datetime
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sklearn.linear_model import LogisticRegression
from sqlalchemy import select, func, case, or_
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import db_helper
from football.fb_dao import TeamDAO
from football.models import Team, Match, Prediction

router = APIRouter(prefix="/prediction", tags=["football"])



# @router.get("/predict/{home_team}/{away_team}", response_model=dict)
# async def predict(home_team: str, away_team: str):
#     """
#     Прогнозирует вероятность победы команды дома против соперника.
#     Возвращает значение вероятности победы домашней команды.
#     """
#     async with db_helper.session_factory() as session:
#         # Выбор статистики побед для двух указанных команд
#         stmt = (
#             select(Team.name.label("team_name"),
#                    func.count(Match.id).label("total_matches"),
#                    func.sum(case((Match.home_score > Match.away_score, 1), else_=0)).label("wins"))
#             .join(Match, or_(Match.team_home_id == Team.id, Match.team_away_id == Team.id))
#             .where(Team.name.in_([home_team, away_team]))
#             .group_by(Team.name)
#         )
#
#         # Выполнение запроса
#         result = await session.execute(stmt)
#         rows = result.all()
#
#         if len(rows) != 2:
#             raise HTTPException(status_code=404, detail="Данные о командах отсутствуют или недостаточны.")
#
#         # Преобразование результата в DataFrame
#         df = pd.DataFrame(rows, columns=["team_name", "total_matches", "wins"])
#         df["win_percentage"] = df["wins"] / df["total_matches"]
#
#         # Обучаем простую модель классификации
#         X_train = df[["win_percentage"]].values.reshape(-1, 1)
#         y_train = [1 if row['team_name'] == home_team else 0 for _, row in df.iterrows()]
#         model = LogisticRegression().fit(X_train, y_train)
#
#         # Формируем предсказание вероятности победы домашней команды
#         prediction = model.predict_proba(df.query(f'team_name == "{home_team}"')[["win_percentage"]])[0][1]
#
#         return {"probability": float(prediction)}
@router.post("/", response_model=dict)
async def predict_match(
        home_team: str,
        away_team: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Прогнозирует вероятность победы домашней команды против соперника.
    Сохраняет предсказание в базу данных.

    Параметры:
    - home_team: название домашней команды
    - away_team: название гостевой команды

    Возвращает:
    - Вероятность победы домашней команды
    - Вероятность ничьей
    - Вероятность победы гостевой команды
    """
    # Получаем данные команд
    stmt = (
        select(Team)
        .where(Team.name.in_([home_team, away_team]))
        .options(
            selectinload(Team.home_matches),
            selectinload(Team.away_matches)
        )
    )
    result = await session.execute(stmt)
    teams = result.scalars().all()

    if len(teams) != 2:
        raise HTTPException(status_code=404, detail="Одна или обе команды не найдены")

    home_team_data = next(t for t in teams if t.name == home_team)
    away_team_data = next(t for t in teams if t.name == away_team)

    # Собираем статистику
    def calculate_stats(team):
        home_wins = sum(1 for m in team.home_matches if m.home_score > m.away_score)
        away_wins = sum(1 for m in team.away_matches if m.away_score > m.home_score)
        total_matches = len(team.home_matches) + len(team.away_matches)
        win_percentage = (home_wins + away_wins) / total_matches if total_matches > 0 else 0.5
        return {
            "team_name": team.name,
            "win_percentage": win_percentage,
            "total_matches": total_matches
        }

    stats = [calculate_stats(home_team_data), calculate_stats(away_team_data)]
    df = pd.DataFrame(stats)

    # Создаем и обучаем модель
    X = df[["win_percentage"]].values.reshape(-1, 1)
    y = [1, 0]  # 1 для home_team, 0 для away_team

    model = LogisticRegression()
    model.fit(X, y)

    # Получаем вероятности
    home_prob = model.predict_proba([[stats[0]["win_percentage"]]])[0][1]
    away_prob = model.predict_proba([[stats[1]["win_percentage"]]])[0][1]
    draw_prob = 1 - (home_prob + away_prob)  # Простое предположение

    # Создаем новый матч (если нужно)
    match = Match(
        home_team_id=home_team_data.id,
        away_team_id=away_team_data.id,
        date=datetime.datetime.now()
    )
    session.add(match)
    await session.commit()
    await session.refresh(match)

    # Сохраняем предсказание
    prediction = Prediction(
        home_win_prob=home_prob,
        draw_prob=draw_prob,
        away_win_prob=away_prob,
        match_id=match.id
    )
    session.add(prediction)
    await session.commit()

    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_win_probability": home_prob,
        "draw_probability": draw_prob,
        "away_win_probability": away_prob
    }

