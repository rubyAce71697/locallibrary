"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^catalog/',include('catalog.urls'))
]

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/catalog/',permanent=True)),
]
"""
urlpatterns += [
    url(r'^accounts/',include('django.contrib.auth.urls'))
]
"""

urlpatterns += [
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
]
print "URL.py MEDIA_URL", settings.MEDIA_URL
print "URL.py MEDIA_ROOT", settings.MEDIA_ROOT

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)


print urlpatterns[-2:]


"""
urlpatterns = patterns('',
               (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
              )
"""