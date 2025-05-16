from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)

    follower = db.relationship("User", foreign_keys=[follower_id])
    followed = db.relationship("User", foreign_keys=[followed_id])

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"), nullable=False)
    author = db.relationship("User", backref="comments")
    post = db.relationship("Post", backref="comments")
    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
    
class media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_url: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"), nullable=False)
    post = db.relationship("Post", backref="media")
    
    def serialize(self):
        return {
            "id": self.id,
            "media_url": self.media_url,
            "post_id": self.post_id,
            "type": self.type,
        }

