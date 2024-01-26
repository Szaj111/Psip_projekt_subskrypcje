import sqlalchemy.orm
import sqlalchemy
Base = sqlalchemy.orm.declarative_base()
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class User(Base):
    __tablename__ = "user2323"
    id= sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("user_id"),autoincrement=True, primary_key=True)
    nick = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    subscription_id = sqlalchemy.Column(sqlalchemy.Integer)
    city = sqlalchemy.Column(sqlalchemy.String)


class Movie(Base):
    __tablename__ = "movies"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("movie2323"), autoincrement=True,primary_key=True)
    movie_name = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    subscription_id = sqlalchemy.Column(sqlalchemy.String)
class Movies_watched(Base):
    __tablename__ = "movies_watched2323"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("movies_watched"), autoincrement=True,primary_key=True)
    movie_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)

class Subscription(Base):
    __tablename__ = "subscriptions2323"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("subscription"), autoincrement=True, primary_key=True)
    subscription = sqlalchemy.Column(sqlalchemy.String)
    movie_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("movies.id"))
    movie = relationship("Movie")

