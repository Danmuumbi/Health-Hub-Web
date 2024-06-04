"""Add Medical_Records table

Revision ID: e8c28675c883
Revises: b1c0d7fc349f
Create Date: 2024-06-04 16:11:30.715145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8c28675c883'
down_revision = 'b1c0d7fc349f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Departments',
    sa.Column('department_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('department_name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('contact_info', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('department_id')
    )
    op.create_table('Appointments',
    sa.Column('appointment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('service_type', sa.String(length=100), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('appointment_id')
    )
    op.create_table('Medical_Records',
    sa.Column('record_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('medical_history', sa.Text(), nullable=True),
    sa.Column('medications', sa.Text(), nullable=True),
    sa.Column('vaccination_record', sa.Text(), nullable=True),
    sa.Column('lab_results', sa.Text(), nullable=True),
    sa.Column('allergies', sa.Text(), nullable=True),
    sa.Column('immunizations', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('record_id')
    )
    op.create_table('Payments',
    sa.Column('payment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('payment_info', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Payments')
    op.drop_table('Medical_Records')
    op.drop_table('Appointments')
    op.drop_table('Departments')
    # ### end Alembic commands ###