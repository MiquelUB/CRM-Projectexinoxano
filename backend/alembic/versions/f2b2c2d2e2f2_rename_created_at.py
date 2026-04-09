"""Rename data_creacio to created_at in V2 tables

Revision ID: f2b2c2d2e2f2
Revises: f1a1b1c1d1e1
Create Date: 2026-04-09 17:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f2b2c2d2e2f2'
down_revision = 'f1a1b1c1d1e1'
branch_labels = None
depends_on = None

def upgrade():
    # Municipis Lifecycle
    op.alter_column('municipis_lifecycle', 'data_creacio', new_column_name='created_at')
    # Contactes V2
    op.alter_column('contactes_v2', 'data_creacio', new_column_name='created_at')

def downgrade():
    op.alter_column('contactes_v2', 'created_at', new_column_name='data_creacio')
    op.alter_column('municipis_lifecycle', 'created_at', new_column_name='data_creacio')
