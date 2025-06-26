from crud.basedao import BaseDAO
from football.models import Prediction, Team, Match


class PredictDAO(BaseDAO):
    model = Prediction


class TeamDAO(BaseDAO):
    model = Team


class MatchDAO(BaseDAO):
    model = Match