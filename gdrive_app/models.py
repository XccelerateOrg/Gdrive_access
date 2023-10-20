from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from gdrive_app import db, app


class VideoPath(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    origin: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    video: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    destin: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user: Mapped[str] = mapped_column(String, unique=False, nullable=False)

    def __repr__(self):
        return f"VideoPath('{self.tag}','{self.video}','{self.destin}', '{self.user})"


with app.app_context():
    db.create_all()

