from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Part(Base):
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lcsc = Column(String, index=True, unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    mfr = Column(String)
    package = Column(String)
    joints = Column(Integer)
    manufacturer = Column(String)
    basic = Column(Boolean)
    description = Column(String)
    datasheet = Column(String)
    stock = Column(Integer)
    price = Column(Float)
    last_update = Column(DateTime, default=datetime.datetime.utcnow)
    resistance = Column(Float, nullable=True, index=True)
    inductance = Column(Float, nullable=True, index=True)
    capacitance = Column(Float, nullable=True, index=True)
    dielectric = Column(String, nullable=True, index=True)
    current = Column(Float, nullable=True, index=True)
    voltage = Column(Float, nullable=True, index=True)

def create_or_update_part(session: Session, part: Part):
    stmt = insert(Part).values(
        lcsc=part.lcsc,
        category_id=part.category_id,
        mfr=part.mfr,
        package=part.package,
        joints=part.joints,
        manufacturer=part.manufacturer,
        basic=part.basic,
        description=part.description,
        datasheet=part.datasheet,
        stock=part.stock,
        price=part.price,
        last_update=part.last_update
    ).on_conflict_do_update(
        index_elements=['lcsc'],
        set_={
            'price': part.price,
            'stock': part.stock,
            'last_update': part.last_update
        }
    )

    session.execute(stmt)
    return part


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    subcategory_name = Column(String)
    parts = relationship('Part', backref='category')

    @property
    def component_count(self):
        return sum([subclass.component_count for subclass in self.subclasses])
    
def create_or_update_category(session: Session, category: Category):
    existing_category = session.query(Category).filter_by(name=category.subcategory_name).first()
    if existing_category:
        existing_category.subcategory_name = category.subcategory_name
        return existing_category
    else:
        category.id = session.add(category)
        session.commit()
        return category