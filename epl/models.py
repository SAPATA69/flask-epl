from epl import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

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
    
    # ✅ เพิ่ม fields ใหม่ที่ templates ต้องการ
    goals: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    squad_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    img: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    club_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('clubs.id'), nullable=True)

    club: Mapped[Optional["Club"]] = relationship("Club", back_populates="players")
    
    def __repr__(self):
        return f"<Player {self.name}>"