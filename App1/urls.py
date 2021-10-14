from django.urls import path
from App1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as v
from django.conf.urls import url
from django.views.static import serve
  

urlpatterns=[
	path('',views.home,name="home"),
	path('fhome/<int:id>/',views.fhome,name="fhome"),
	path('flogin',views.flogin,name="flogin"),
	path("createtest/<int:fid>/",views.createtest,name="createtest"),
	path("studentsupload/<int:fid>/<int:eid>/",views.studentsupload,name="studentsupload"),
	path("facultyupload",views.facultyupload,name="facultyupload"),
	path("AddQuestions/<int:fid>/<int:eid>/<int:k>/",views.AddQuestions,name="AddQuestions"),
	path("StudRegistration",views.StudRegistration,name="StudRegistration"),
	path('slogin',views.slogin,name="slogin"),
	path('studentExam/<str:semail>/',views.studentExam,name="studentExam"),
	path('examopen/<int:sid>/<int:eid>/',views.examopen,name="examopen"),
	path("modifytest/<int:fid>/",views.modifytest,name="modifytest"),
	path("specificTestModify/<int:eid>/",views.specificTestModify,name="specificTestModify"),
	path("specificTestDelete/<int:eid>/",views.specificTestDelete,name="specificTestDelete"),
	path('adminlogin',views.adminlogin,name="adminlogin"),
	path('adminpage',views.adminpage,name="adminpage"),
	path('facultyModify',views.facultyModify,name="facultyModify"),
	path('viewFaculty',views.viewFaculty,name="viewFaculty"),
	path('facrowUpdate/<int:id>/',views.facrowUpdate,name="facrowUpdate"),
	path('facrowDelete/<int:id>/',views.facrowDelete,name="facrowDelete"),
	path('results/<int:fid>/',views.results,name="results"),
	path('displayTestResult/<int:eid>/',views.displayTestResult,name="displayTestResult"),
	path('downloadResults/<int:eid>/',views.downloadResults,name="downloadResults"),
	path('OneQuestion/<int:i>/',views.OneQuestion,name="OneQuestion"),

]