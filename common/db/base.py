from sqlalchemy.orm import declarative_base

# Single declarative Base for all models. Engine/session are defined in common.db.engine/session
Base = declarative_base()
