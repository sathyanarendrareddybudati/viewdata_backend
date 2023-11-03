from django.db import models

class Dataset(models.Model):
    
    id = models.AutoField(db_column='uid', primary_key=True)
    name = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
