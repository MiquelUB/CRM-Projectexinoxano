"""Add activitats_municipi table indexes

Revision ID: f1a1b1c1d1e1
Revises: e40234ee066b
Create Date: 2026-04-09 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1a1b1c1d1e1'
down_revision = 'a3f5e76d049d'
branch_labels = None
depends_on = None

def upgrade():
    # Crear la taula si no existeix (per si fix_schema no s'ha executat o ha fallat)
    op.execute("""
        CREATE TABLE IF NOT EXISTS activitats_municipi (
            id UUID PRIMARY KEY,
            municipi_id UUID NOT NULL REFERENCES municipis_lifecycle(id),
            contacte_id UUID REFERENCES contactes_v2(id),
            deal_id UUID,
            tipus_activitat VARCHAR(50) NOT NULL,
            data_activitat TIMESTAMPTZ NOT NULL,
            contingut JSONB DEFAULT '{}',
            notes_comercial TEXT,
            generat_per_ia BOOLEAN DEFAULT FALSE,
            etiquetes TEXT[],
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Afegir índexs
    op.create_index(op.f('ix_activitats_municipi_municipi_id'), 'activitats_municipi', ['municipi_id'], unique=False)
    op.create_index(op.f('ix_activitats_municipi_data_activitat'), 'activitats_municipi', ['data_activitat'], unique=False)
    op.create_index(op.f('ix_activitats_municipi_tipus_activitat'), 'activitats_municipi', ['tipus_activitat'], unique=False)
    
    # GIN Index
    op.execute("CREATE INDEX IF NOT EXISTS ix_activitats_contingut_gin ON activitats_municipi USING gin (contingut)")

def downgrade():
    op.drop_index('ix_activitats_contingut_gin', table_name='activitats_municipi')
    op.drop_index(op.f('ix_activitats_municipi_tipus_activitat'), table_name='activitats_municipi')
    op.drop_index(op.f('ix_activitats_municipi_data_activitat'), table_name='activitats_municipi')
    op.drop_index(op.f('ix_activitats_municipi_municipi_id'), table_name='activitats_municipi')
