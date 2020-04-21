from django import forms
from .models import User_Profile, Query_Profile

#DataFlair #File_Upload

class Profile_Form(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
        'studies',
        'species',
        'corr_file',
        'knowledge_capture_sample_file',
        'knowledge_capture_gene_file',
        'additional_filter_file',
        'email',
        'tag',
        ]

class Query_Form(forms.ModelForm):
    class Meta:
        model = Query_Profile
        fields = [
        'studies',
        'species',
        ]
