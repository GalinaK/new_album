__author__ = 'galina'
from album.models import *

def category(request):
	return {'number': Category.objects.all()}

def photo1(request):
	return{'image_url': Image.objects.all().order_by('id_photo_gallery')}

def photo2(request):
	return{'photo_album': Image.objects.all().order_by('main_photo')}
