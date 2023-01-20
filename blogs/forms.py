
from django import forms
from .models import Post, BlogComment,ReplayComment,SubcribeUsers,Contact
from ckeditor.fields import RichTextField
from taggit.forms import TagWidget

class DateInput(forms.DateInput):
    input_type = 'date'
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['post_id','thumbnail','co_author','writer_name','category','title','content','post_date','tags']

        widgets={
        'post_id': forms.TextInput(attrs={'class':'form-control form-admin'}),
        'writer_name': forms.TextInput(attrs={'class':'form-control form-admin'}),
        'co_author': forms.TextInput(attrs={'class':'form-control form-admin'}),

        'title': forms.TextInput(attrs={'class':'form-control form-admin'}),
        #'discription':forms.Textarea(attrs={'class':'form-control'}),
        'content': RichTextField(),
        'tags': TagWidget(attrs={'class':'form-control form-admin'}),
        'category': forms.Select(attrs={'class':'form-control  form-admin form-cat'}),
        'post_date':DateInput()

    }



class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubcribeUsers
        fields=['email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields=['name','email','phone',"message"]
        widgets={
              'name':forms.TextInput(attrs={'class':'form-control','style':'border-style: outset;','placeHolder':"Enter Name"}),
              'email':forms.TextInput(attrs={'class':'form-control','style':'border-style: outset;','placeHolder':"Enter Email"}),
             'phone':forms.TextInput(attrs={'class':'form-control','style':'border-style: outset;','placeHolder':"Enter Phone no.",'max-length':12}),
             'message':forms.Textarea(attrs={'class':'form-control','style':'border-style: outset;','placeHolder':"Enter Message"}),


        }