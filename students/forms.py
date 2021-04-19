from django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)

    # You are going to use this form for students to enroll on courses. The course field is
    # for the course on which the user will be enrolled; therefore, it's a ModelChoiceField.
    # You use a HiddenInput widget because you are not going to show this field to
    # the user. You are going to use this form in the CourseDetailView view to display
    # a button to enroll