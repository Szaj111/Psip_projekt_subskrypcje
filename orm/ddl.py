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

    watched_movies = relationship("Movies_watched", back_populates="user")

class Movie(Base):
    __tablename__  = "movies"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("movie2323"), autoincrement=True,primary_key=True)
    movie_name = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)


    watched_movies = relationship("Movies_watched", back_populates="movie")
class Movies_watched(Base):
    __tablename__ = "movies_watched2323"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("movies_watched"), autoincrement=True, primary_key=True)
    movie_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("movies.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user2323.id"))
    category = sqlalchemy.Column(sqlalchemy.String)

    user = relationship("User", back_populates="watched_movies")
    movie = relationship("Movie", back_populates="watched_movies")

    def __repr__(self):
        return f"<Movies_watched(user_id={self.user_id}, movie_id={self.movie_id}, category_id={self.category_id})>"


class Subscription(Base):
    __tablename__ = "subscriptions2323"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence("subscription"), autoincrement=True, primary_key=True)
    subscription = sqlalchemy.Column(sqlalchemy.String)
    movie_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("movies.id"))
    movie = relationship("Movie")


