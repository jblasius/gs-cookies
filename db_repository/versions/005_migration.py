from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
async_operation = Table('async_operation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('async_operation_status_id', Integer),
    Column('user_profile_id', Integer),
)

async_operation_status = Table('async_operation_status', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('code', String(length=20)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_name', String(length=64)),
    Column('last_seen', DateTime),
    Column('social_id', String(length=64)),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['async_operation'].create()
    post_meta.tables['async_operation_status'].create()
    post_meta.tables['user'].columns['email'].create()
    post_meta.tables['user'].columns['first_name'].create()
    post_meta.tables['user'].columns['last_name'].create()
    post_meta.tables['user'].columns['social_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['async_operation'].drop()
    post_meta.tables['async_operation_status'].drop()
    post_meta.tables['user'].columns['email'].drop()
    post_meta.tables['user'].columns['first_name'].drop()
    post_meta.tables['user'].columns['last_name'].drop()
    post_meta.tables['user'].columns['social_id'].drop()
