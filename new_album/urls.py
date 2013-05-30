from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'new_album.views.home', name='home'),
    # url(r'^new_album/', include('new_album.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^base/$', "album.views.base"),
	url(r'^main/$', "album.views.main"),

	url(r'^main/(\d+)/$', "album.views.album"),
	url(r'^main/image/(\d+)/$', "album.views.image"),
	url(r"^(\d+)/(full|thumbnails)/$", "album.views.album"),
	url(r"^(\d+)/(full|thumbnails|edit)/$", "album.views.album"),
	url(r'^gallery/$', "album.views.gallery_photo"),
	url(r'^slider/$', "album.views.slider"),
	url(r'^slider2/$', "album.views.slider2"),
#	url(r'^test3/$', "album.views.test4"),
)
