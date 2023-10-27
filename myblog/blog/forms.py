from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'main_image', 'is_published']
        labels = {
            'title': 'Title',
            'content': 'Content',
            'main_image': 'Main Image URL',
            'is_published': 'Publish',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(attrs={'class': 'ckeditor form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'published_check_section_edit'}),
        }

class EditBlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'main_image', 'is_published']
        labels = {
            'title': 'Title',
            'content': 'Content',
            'main_image': 'Main Image URL',
            'is_published': 'Publish',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(attrs={'class': 'ckeditor form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'published_check_section_edit'}),
        }
        
class EmailBlogForm(forms.Form):
    sender_name = forms.CharField(max_length=100)
    sender_email = forms.EmailField()
    recipient_email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)        
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']