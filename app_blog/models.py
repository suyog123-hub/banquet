from django.db import models
from config.basemodel import Base
from django.conf import settings
class BlogCategory(Base):
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title
class Content(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='blog_content')
    title = models.ForeignKey(BlogCategory,on_delete=models.CASCADE,null=True)
    heading = models.CharField(max_length=200,null=True)
    date = models.DateField()
    image = models.ImageField(upload_to='blogimage',null=True)
    content = models.TextField(help_text="upload here your content",null=True , blank=True)

    def __str__(self):
        return  self.heading
class Comment(Base):
    blog = models.ForeignKey(Content,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comments")
    text = models.TextField()
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} comment on  - {self.blog.title}"
    
    
    