"""add_agent_memory_v2

Revision ID: 737f14652d0c
Revises: 96cbc1328ae4
Create Date: 2026-04-10 18:26:06.831402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '737f14652d0c'
down_revision: Union[str, Sequence[str], None] = '96cbc1328ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('agent_memories_v2',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('municipi_id', sa.UUID(), nullable=True),
    sa.Column('usuari_id', sa.UUID(), nullable=False),
    sa.Column('deal_id', sa.UUID(), nullable=True),
    sa.Column('session_id', sa.UUID(), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('history', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('clau', sa.String(length=50), nullable=True),
    sa.Column('valor', sa.Text(), nullable=True),
    sa.Column('confianca', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['municipi_id'], ['municipis_lifecycle.id'], ),
    # sa.ForeignKeyConstraint(['usuari_id'], ['usuaris.id'], ), # Eliminat per evitar error f405 (Desacoblament V1/V2)
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_memories_v2_clau'), 'agent_memories_v2', ['clau'], unique=False)
    op.create_index(op.f('ix_agent_memories_v2_session_id'), 'agent_memories_v2', ['session_id'], unique=False)
    op.create_index(op.f('ix_agent_memories_v2_usuari_id'), 'agent_memories_v2', ['usuari_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_agent_memories_v2_session_id'), table_name='agent_memories_v2')
    op.drop_index(op.f('ix_agent_memories_v2_clau'), table_name='agent_memories_v2')
    op.drop_table('agent_memories_v2')
    # ### end Alembic commands ###
