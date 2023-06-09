from django.db import models
from log_reg_app.models import User



class MessageManager(models.Manager):
    def validator_msg(self, postData):
        errors = {}
        if len(postData['message']) < 1:
            errors["empty_msg"] = "You can't post an empty message"
        return errors


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()


class CommentManager(models.Manager):
    def validator_cmt(self, postData):
        errors = {}
        if len(postData['comment']) < 1:
            errors["empty_cmt"] = "You can't post an empty comment"
        return errors


class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
