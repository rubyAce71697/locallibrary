from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    url(r'^home/$',views.index ,name='index'),
    url(r'^book/$',views.BooksListView.as_view(),name='book'),
    url(r'^book/(?P<pk>\d+)$',views.BooksDetailView.as_view(),name='book-detail'),
    url(r'^author/$',views.AuthorListView.as_view(),name='author'),
    url(r'author/(?P<pk>\d+)$',views.AuthorDetailView.as_view(),name='author-detail'),

    url(r'^register/$',views.register, name='register'),
    url(r'^login/$',views.user_login,   name='login'),
    url(r'^$', views.user_login,  name='login'),
    url(r'^logout/$',auth_views.logout,  {'next_page':'/catalog/'}, name='logout'),
 

]

urlpatterns += [
    url(r'^mybooks/',views.LoanedBooksByUserListView.as_view(),name='my-borrowed')
]
urlpatterns += [
    url(r'^booksloaned/',views.AllLoanedBooksListView,name='all-borrowed')
]

urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$',views.renew_book_librarian,name='renew-book-librarian')
]


urlpatterns += [
    url(r'^book/create/$',views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)$/update',views.AuthorUpdate.as_view(),name = 'author_update'),
    url(r'^author/(?P<pk>\d+)$/delete',views.AuthorDelete.as_view(),name='author_delete')
]

urlpatterns += [
    url(r'^ajax/bookmarks/$', views.get_bookmarks, name='fetch_bookmarks')
]

urlpatterns += [
    url(r'^ajax/bookmarked/$', views.ifbookmarked, name='check_bookmarks')
]
urlpatterns += [
    url(r'^ajax/issued/$', views.ifIssued, name='check_issue')
]

urlpatterns += [
    url(r'^ajax/bookmarkme/$', views.bookmarkme, name='check_issue')
]

urlpatterns += [
    url(r'^defaulters/$', views.get_defaulters, name='all-defaulters')
]

urlpatterns += [
    url(r'^profile/(?P<username>\w+)$', views.user_profile, name='user-profile')
]

urlpatterns += [
    url(r'^search$', views.search, name='search')
]
urlpatterns += [
    url(r'^issue$', views.issue, name='issue')
]
urlpatterns += [
    url(r'^ajax/verify/$', views.verify_get_instances, name='v_g_instances')
]
urlpatterns += [
    url(r'^ajax/issue/$', views.issue_book, name='issue_instance')
]
