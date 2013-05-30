from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from new_album.settings import MEDIA_URL
from django.core.context_processors import csrf
from django.template import *
from django.http import HttpRequest
from album.models import *
from django.db import connection, transaction
from new_album.settings import TEMPLATE_DIRS


def main(request):
	"""Main listing."""

	albums = Album.objects.all()
	if not request.user.is_authenticated():
		albums = albums.filter(public=True)

	paginator = Paginator(albums, 10)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	try:
		albums = paginator.page(page)
	except (InvalidPage, EmptyPage):
		albums = paginator.page(paginator.num_pages)

	for album in albums.object_list:
		album.images = album.image_set.all()[:4]

	cursor = connection.cursor()
	a = Image.objects.raw(
		'''SELECT album_image. * , album_image_albums. *, album_album.* FROM album_image INNER JOIN album_image_albums ON album_image.id = album_image_albums.image_id inner join album_album on album_album.id = album_image_albums.album_id where main_photo=1 ''')

	#	return render_to_response("photo/main.html", dict(albums=albums,
	#	user=request.user, media_url=MEDIA_URL))
	return render(request, 'photo/main.html', {'albums': albums, 'main_a': a})


def base(request):
	return render(request, 'base.html', {})


def slider(request):
	return render(request, 'photo/big_slider.html', {})

def slider2(request):
	return render(request, 'photo/big_slider2.html', {})


def album(request, pk, view="thumbnails"):
	"""Album listing."""
	#	main_photo = Image.objects.all().order_by('main_photo')
	num_images = 30
	if view == "full": num_images = 1
	#	albums = Album.objects.all()


	album = Album.objects.get(pk=pk)
	images = album.image_set.all()
	paginator = Paginator(images, num_images)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		images = paginator.page(page)
	except (InvalidPage, EmptyPage):
		images = paginator.page(paginator.num_pages)


	# add list of tags as string and list of album objects to each image object
	for img in images.object_list:
		tags = [x[1] for x in img.tags.values_list()]
		img.tag_lst = join(tags, ', ')
		img.album_lst = [x[1] for x in img.albums.values_list()]

		d = dict(album=album, images=images, user=request.user, view=view,
			albums=Album.objects.all(), media_url=MEDIA_URL)
		d.update(csrf(request))
		return  render(request, 'photo/album.html', d)


def image(request, pk):
	""" Image page
	"""
	img = Image.objects.get(pk=pk)
	return render_to_response("photo/image.html", dict(image=img,
		user=request.user, media_url=MEDIA_URL))

#
#	return render_to_response("photo/image.html", dict(image=img,
#		user=request.user, backurl=request.META["HTTP_REFERER"],
#		media_url=MEDIA_URL))


def gallery_photo(request):
	return render(request, 'photo/gallery_photo.html', {})


#def test4(request):
#
#	cursor = connection.cursor()
#
#	a = Image.objects.raw('''SELECT album_image. * , album_image_albums. *, album_album.* FROM album_image INNER JOIN album_image_albums ON album_image.id = album_image_albums.image_id inner join album_album on album_album.id = album_image_albums.album_id where main_photo=1 ''')
##	cursor.excute("SELECT album_image.*, album_album.title_album FROM album_image LEFT JOIN album_album ON album_image.id = album_album.id")
#	return render(request, 'photo/test4.html',{'main_a': a})
