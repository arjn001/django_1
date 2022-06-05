from django.shortcuts import render,redirect
from django.views import View
from .models import *
# Create your views here.

class BaseView(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['subcategories'] = SubCategory.objects.all()

	
class HomeView(BaseView):
	def get(self,request):
		
		self.views['new_products'] = Product.objects.filter(labels = 'new')
		self.views['hot_products'] = Product.objects.filter(labels = 'hot')
		self.views['offer_products'] = Product.objects.filter(labels = 'offer')
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		return render(request,'index.html', self.views)


class SubCategoryView(BaseView):
	def get(self,request,slug):
		sub_cat = SubCategory.objects.get(slug = slug).id
		self.views['subcat_products'] = Product.objects.filter(subcategory_id = sub_cat)
		return render(request,'subcategory.html', self.views)


class DetailView(BaseView):
	def get(self,request,slug):
		self.views['detail_products'] = Product.objects.filter(slug = slug)
		return render(request,'single.html', self.views)

from django.db.models import Q
class SearchView(BaseView):
	def get(self,request):
		query = request.GET['query']
		if query == '':
			return redirect('/')
		lookups = Q(name__icontains = query) | Q(description__icontains = query)
		self.views['search_result'] = Product.objects.filter(lookups).distinct()
		self.views['search.for'] = query
		return render(request,'search.html', self.views)


