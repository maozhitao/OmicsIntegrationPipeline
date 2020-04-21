from django.db import models

class User_Profile(models.Model):
    studies     = models.CharField(max_length=200)
    species     = models.CharField(max_length = 200)
    corr_file   = models.FileField()
    knowledge_capture_sample_file = models.FileField()
    knowledge_capture_gene_file = models.FileField()
    additional_filter_file = models.FileField()
    tag	= models.CharField(max_length=200, default = None)
    email = models.EmailField(default = None)
    
    
    def __str__(self):
        return self.studies

class Query_Profile(models.Model):
    studies    = models.CharField(max_length=200)
    species    = models.CharField(max_length=200)

    def __str__(self):
        return self.studies
