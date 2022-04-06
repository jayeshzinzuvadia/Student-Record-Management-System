from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'student'
urlpatterns = [
    path('all', views.studentsList, name='allstudentslist'),
    path('search', views.SearchStudentView.as_view(), name='searchstudent'),
    path('filters', views.viewFilterStudent, name='filterstudent'),
    path('filterResults', views.ViewFilterResults.as_view(), name='filterresults'),
    path('new', views.viewAddStudent, name='addstudent'),
    path('uploadFile', views.viewUploadFile, name='uploadfile'),
    path('postUploadFile', views.postUploadFile, name='postuploadfile'),
    path('registerStudent', views.addStudent, name='registerstudent'),
    path('view/?P<id>', views.ViewStudentRecord.as_view(), name='viewstudent'),
    path('update/?P<id>', views.UpdateStudentRecord.as_view(), name='updatestudent'),
    path('updateStudent/', views.updateStudent, name='updatestudentinfo'),
    path('updateMultipleStudents/', views.viewUpdateMultipleStudentRecords, name='updatemultiplestudentrecords'),
    path('postUpdateMultipleStudents/', views.postUpdateMultipleStudentRecords, name='postupdatemultiplestudentrecords'),
    path('delete/?P<id>', views.DeleteStudentRecord.as_view(), name='deletestudent'),
    path('deleteStudent/', views.deleteStudent, name='removestudent'),
    path('pageNotFound/', views.pageNotFound, name='pagenotfound'),
]

if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)