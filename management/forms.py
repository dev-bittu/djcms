from django import forms
from ckeditor.widgets import CKEditorWidget

class CKEditorForm(forms.Form):
    content = forms.CharField(widget = CKEditorWidget())
