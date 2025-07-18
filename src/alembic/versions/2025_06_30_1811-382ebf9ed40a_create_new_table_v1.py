"""“Create_new_table_v1”

Revision ID: 382ebf9ed40a
Revises: 
Create Date: 2025-06-30 18:11:00.786267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '382ebf9ed40a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_teams')),
    sa.UniqueConstraint('name', name=op.f('uq_teams_name'))
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=True),
    sa.Column('away_score', sa.Integer(), nullable=True),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['teams.id'], name=op.f('fk_matches_away_team_id_teams')),
    sa.ForeignKeyConstraint(['home_team_id'], ['teams.id'], name=op.f('fk_matches_home_team_id_teams')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_matches'))
    )
    op.create_table('predictions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home_win_prob', sa.Float(), nullable=False),
    sa.Column('draw_prob', sa.Float(), nullable=False),
    sa.Column('away_win_prob', sa.Float(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], name=op.f('fk_predictions_match_id_matches'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_predictions'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('predictions')
    op.drop_table('matches')
    op.drop_table('teams')
    # ### end Alembic commands ###
