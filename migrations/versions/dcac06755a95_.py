"""empty message

Revision ID: dcac06755a95
Revises: 3fc5958ddcb2
Create Date: 2018-01-09 15:01:57.339470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcac06755a95'
down_revision = '3fc5958ddcb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('cat_1', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('cat_2', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('cat_3', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('cat_4', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('cat_5', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('review_avg', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('review_date', sa.DateTime(), nullable=False))
    op.add_column('reviews', sa.Column('reviewer_id', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('visited_date', sa.DateTime(), nullable=False))
    op.create_foreign_key(None, 'reviews', 'user', ['reviewer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'visited_date')
    op.drop_column('reviews', 'reviewer_id')
    op.drop_column('reviews', 'review_date')
    op.drop_column('reviews', 'review_avg')
    op.drop_column('reviews', 'cat_5')
    op.drop_column('reviews', 'cat_4')
    op.drop_column('reviews', 'cat_3')
    op.drop_column('reviews', 'cat_2')
    op.drop_column('reviews', 'cat_1')
    # ### end Alembic commands ###
