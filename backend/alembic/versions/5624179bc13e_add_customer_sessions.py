"""add customer sessions

Revision ID: 5624179bc13e
Revises: 7f6a09d64a3a
Create Date: 2026-08-20 19:24:00.875283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5624179bc13e'
down_revision: Union[str, Sequence[str], None] = '7f6a09d64a3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add session_id temporarily as nullable
    op.add_column(
        'customer_messages',
        sa.Column('session_id', sa.Integer(), nullable=True)
    )

    # 2. customer_sessions already exists in the database.
    # Create one session for each agent that has existing messages.
    op.execute("""
        INSERT INTO customer_sessions (agent_id, created_at, updated_at)
        SELECT
            agent_id,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        FROM customer_messages
        WHERE agent_id IS NOT NULL
        GROUP BY agent_id
    """)

    # 3. Attach existing messages to their agent's session
    op.execute("""
        UPDATE customer_messages cm
        SET session_id = cs.id
        FROM customer_sessions cs
        WHERE cm.agent_id = cs.agent_id
          AND cm.session_id IS NULL
    """)

    # 4. Now session_id can be required
    op.alter_column(
        'customer_messages',
        'session_id',
        existing_type=sa.Integer(),
        nullable=False
    )

    # 5. Add foreign key
    op.create_foreign_key(
        'fk_customer_messages_session_id',
        'customer_messages',
        'customer_sessions',
        ['session_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # 6. Add index
    op.create_index(
        'ix_customer_messages_session_id',
        'customer_messages',
        ['session_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        'ix_customer_messages_session_id',
        table_name='customer_messages'
    )

    op.drop_constraint(
        'fk_customer_messages_session_id',
        'customer_messages',
        type_='foreignkey'
    )

    op.drop_column(
        'customer_messages',
        'session_id'
    )

    