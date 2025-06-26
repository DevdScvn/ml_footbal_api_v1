from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Prediction(Base):

    match_id: Mapped[int] = mapped_column(primary_key=True)
    team: Mapped[str]
    opponent: Mapped[str]
    win_probability: Mapped[float]
    predicted_winner: Mapped[str]


class Team(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    total_wins: Mapped[int]

    # Связь "один ко многим" с матчами
    # home_matches = relationship("Match", foreign_keys="Match.home_team_id")
    # away_matches = relationship("Match", foreign_keys="Match.away_team_id")


class Match(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date]

    # Внешние ключи
    # home_team_id = Column(Integer, ForeignKey("teams.id"))
    # away_team_id = Column(Integer, ForeignKey("teams.id"))
    # winner_id = Column(Integer, ForeignKey("teams.id"))

    # Статистика
    home_goals: Mapped[int]
    away_goals: Mapped[int]
    is_home_advantage: Mapped[bool]

    # Связи
    # home_team = relationship("Team", foreign_keys=[home_team_id])
    # away_team = relationship("Team", foreign_keys=[away_team_id])
    # winner = relationship("Team", foreign_keys=[winner_id])