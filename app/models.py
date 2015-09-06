from django.db import models

# Create your models here.

class Conversation(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    duration = models.IntegerField(db_index=True)
    
    def __unicode__(self):
        return "Conversation created at %s" % (self.date)

class DialogueBlock(models.Model):
    content = models.TextField()
    position = models.IntegerField(db_index=True)
    conversation = models.ForeignKey(Conversation, db_index=True)
    speaker = models.TextField()

    def __unicode__(self):
        return "%s -> %s, speaker id = %s id = %s" %(self.position, self.content, self.speaker, self.conversation.id)

