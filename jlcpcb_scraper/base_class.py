from typing import Any

from sqlalchemy.orm import Session, relationship
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_writeable_properties(cls):
        '''Return a dict because a lookup is O(1) in a hashmap and O(n) in a list'''
        relationships = { x : None for x in inspect(cls).relationships.keys() }
        return {
            attr : None for attr, value in vars(cls).items() if 
                attr not in relationships and 
                ((isinstance(value, property) and value.fset is not None) or isinstance(value, InstrumentedAttribute))
            
        }

    @classmethod
    def approx_rowcount(cls, db : Session) -> int:
        result = db.execute(f"""SELECT
            (reltuples/relpages) * (
                pg_relation_size('{cls.__tablename__}') /
                (current_setting('block_size')::integer)
            )
            FROM pg_class where relname = '{cls.__tablename__}';"""
        ).scalar()
        return int(result)

    def as_dict(self) -> dict:
        return {
            col.name: getattr(self, col.name) for col in self.__table__.columns
        }
