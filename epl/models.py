from epl import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Club(db.Model):
    __tablename__ = 'clubs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    stadium: Mapped[str] = mapped_column(String(50), nullable=False)
    founded_year: Mapped[int] = mapped_column(Integer, nullable=False)
    logo: Mapped[str] = mapped_column(String(255), nullable=False)

    players: Mapped[List["Player"]] = relationship("Player", back_populates="club")

    def __repr__(self):
        return f"<Club {self.name}>"

class Player(db.Model):
    __tablename__ = 'players'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('clubs.id'))

    club: Mapped["Club"] = relationship("Club", back_populates="players")
    
    def __repr__(self):
        return f"<Player {self.name}>"
