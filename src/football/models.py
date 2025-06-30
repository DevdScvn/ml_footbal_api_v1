import datetime
from datetime import date
from typing import Optional, List

from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # Связи для домашних и гостевых матчей (раздельные)
    home_matches: Mapped[list["Match"]] = relationship(
        back_populates="home_team",
        foreign_keys="Match.home_team_id"  # Явное указание
    )
    away_matches: Mapped[list["Match"]] = relationship(
        back_populates="away_team",
        foreign_keys="Match.away_team_id"  # Явное указание
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    home_score: Mapped[int] = mapped_column(nullable=True)
    away_score: Mapped[int] = mapped_column(nullable=True)

    # Внешние ключи с явным указанием таблицы
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # Связи с явным указанием foreign_keys
    home_team: Mapped["Team"] = relationship(
        back_populates="home_matches",
        foreign_keys=[home_team_id]  # Критически важно
    )
    away_team: Mapped["Team"] = relationship(
        back_populates="away_matches",
        foreign_keys=[away_team_id]  # Критически важно
    )

    # Связь с предсказаниями
    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_win_prob: Mapped[float]
    draw_prob: Mapped[float]
    away_win_prob: Mapped[float]

    # Внешний ключ
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))

    # Связь
    match: Mapped["Match"] = relationship(back_populates="predictions")

# class Prediction(Base):
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     home_win_prob: Mapped[float]
#     draw_prob: Mapped[float]
#     away_win_prob: Mapped[float]
#
#     match_id: Mapped[int] = mapped_column(ForeignKey("matchs.id", ondelete="CASCADE"))
#     match: Mapped["Match"] = relationship("Match", back_populates="predictions")
#
#
# class Match(Base):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
#     date: Mapped[date]
#
#     home_team: Mapped["Team"] = relationship("Team",  back_populates="home_matches")
#     away_team: Mapped["Team"] = relationship("Team",  back_populates="away_matches")
#
#     predictions: Mapped["Prediction"] = relationship(
#         back_populates="match",
#         cascade="all, delete-orphan"
#     )
#
# class Team(Base):
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#
#     home_matches: Mapped[List["Match"]] = relationship(
#         back_populates="home_team",
#     )
#     away_matches: Mapped[List["Match"]] = relationship(
#         back_populates="away_team",
#     )

# class Team(Base):
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#
# class Match(Base):
#     __tablename__ = "matchs"
#
#     id = Column(Integer, primary_key=True)
#     team_home_id = Column(Integer, ForeignKey("teams.id"))
#     team_away_id = Column(Integer, ForeignKey("teams.id"))
#     home_score = Column(Integer)
#     away_score = Column(Integer)
#     played_at = Column(DateTime)
#
#     # Задаваем foreign_keys явно для предотвращения AmbiguousForeignKeysError
#     team_home = relationship("Team", foreign_keys=[team_home_id], backref="home_matchs")  # Команда-хозяин
#     team_away = relationship("Team", foreign_keys=[team_away_id], backref="away_matchs")  # Команда-гость
#
#
# class Prediction(Base):
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     match_id: Mapped[int] = mapped_column(ForeignKey("matchs.id"), nullable=False)
#     predicted_winner_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
#     probability: Mapped[float] = mapped_column(nullable=False)
#
#     match: Mapped["Match"] = relationship(back_populates="predictions")
#     winner: Mapped["Team"] = relationship(back_populates="winner_predictions")
