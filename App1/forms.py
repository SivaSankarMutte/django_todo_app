from App1.models import Faculty,ExamDetails,Questions,StudentRegistration
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class FacultyForm(forms.ModelForm):
	class Meta:
		model=Faculty
		fields="__all__"
		widgets={
			'email':forms.EmailInput(attrs={
				'class':"form-control my-2",
				'placeholder':"Enter Email",
				}),
			'psw':forms.PasswordInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Password',
				}),
		}

class ExamDetailsForm(forms.ModelForm):
	class Meta:
		model=ExamDetails
		fields=['examName','noOfQuestions']
		widgets={
			'examName':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':"Enter Exam Name",
				}),
			'noOfQuestions':forms.NumberInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter No of Questions',
				}),
		}


class QuestionsForm(forms.ModelForm):
	class Meta:
		model=Questions
		fields=['Question','opt1','opt2','opt3','opt4','ans','qmarks']
		widgets={
			'Question':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':"Enter Question",
				}),
			'opt1':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Option1',
				}),
			'opt2':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Option2',
				}),
			'opt3':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Option3',
				}),
			'opt4':forms.TextInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Option4',
				}),
			'ans':forms.NumberInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Answer',
				}),
			'qmarks':forms.NumberInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Question Marks (Weightage)',
				}),
		}


class StudentRegistrationForm(forms.ModelForm):
	class Meta:
		model=StudentRegistration
		fields="__all__"
		widgets={
			'sname' :forms.TextInput(attrs={
				'class':'form-control my-2',
				'placeholder':'Enter Your Name',
				}),
			'regdno':forms.TextInput(attrs={
				'class':'form-control my-2',
				'placeholder':'Enter Your Regd No',
				}),
			'rollno':forms.NumberInput(attrs={
				'class':'form-control my-2',
				'placeholder':'Enter Your Roll No',
				}),
			'semail':forms.EmailInput(attrs={
				'class':"form-control my-2", 
				'placeholder':"Enter Email",
				}),
			'spsw':forms.PasswordInput(attrs={
				'class':"form-control my-2",
				'placeholder':'Enter Password',
				}),
		}
