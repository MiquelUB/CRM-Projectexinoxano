"""add_agent_memory_v2

Revision ID: 737f14652d0c
Revises: 96cbc1328ae4
Create Date: 2026-04-10 18:26:06.831402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '737f14652d0c'
down_revision: Union[str, Sequence[str], None] = '96cbc1328ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema amb verificació d'existència i sense FKs conflictives."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    tables = inspector.get_table_names()

    # Només creem la taula si no existeix (evita l'error DuplicateTable)
    if 'agent_memories_v2' not in tables:
        op.create_table('agent_memories_v2',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('municipi_id', sa.UUID(), nullable=True),
            # NOT NULL relaxat per usuari_id per donar marge a l'agent global
            sa.Column('usuari_id', sa.UUID(), nullable=True),
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
            # S'HAN ELIMINAT LES FOREIGN KEYS D'AQUESTA MIGRACIÓ (FIX f405)
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_agent_memories_v2_clau'), 'agent_memories_v2', ['clau'], unique=False)
        op.create_index(op.f('ix_agent_memories_v2_session_id'), 'agent_memories_v2', ['session_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    
    if 'agent_memories_v2' in inspector.get_table_names():
        op.drop_index(op.f('ix_agent_memories_v2_session_id'), table_name='agent_memories_v2')
        op.drop_index(op.f('ix_agent_memories_v2_clau'), table_name='agent_memories_v2')
        op.drop_table('agent_memories_v2')
