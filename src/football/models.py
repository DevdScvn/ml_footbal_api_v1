import datetime
from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Prediction(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    home_win_prob: Mapped[float]
    draw_prob: Mapped[float]
    away_win_prob: Mapped[float]

    match_id: Mapped[int] = mapped_column(ForeignKey("matchs.id", ondelete="CASCADE"))
    match: Mapped["Match"] = relationship("Match", back_populates="predictions", lazy="joined")


class Match(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    date: Mapped[date]

    home_team: Mapped["Team"] = relationship("Team",  back_populates="matchs", lazy="joined")
    away_team: Mapped["Team"] = relationship("Team",  back_populates="matchs", lazy="joined")

    predictions: Mapped["Prediction"] = relationship(
        back_populates="matchs",
        cascade="all, delete-orphan"
    )

class Team(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    home_matches: Mapped["Match"] = relationship(
        back_populates="teams",
        foreign_keys="matchs.home_team_id"
    )
    away_matches: Mapped["Match"] = relationship(
        back_populates="teams",
        foreign_keys="matchs.away_team_id"
    )