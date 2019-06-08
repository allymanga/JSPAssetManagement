from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

from .forms import AssetModelForm, CategoryModelForm

from .models import Asset, Category

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    DeleteView
    )

from django.views.generic.edit import UpdateView

from django.urls import reverse 

# Create your views here.
def index(request):
    temp = 'index.html'
    title = "JSP"
    context = {'title':title}
    return render(request,temp,context)

@login_required(login_url='../accounts/login/')
def thank_you(request):
    temp = 'reports/thank_you.html'
    title = "JSP"
    #categories
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    context = {
        'title':title,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
        }
    return render(request,temp,context)

@login_required(login_url='../accounts/login/')
def register(request):
    #recent item

    try:
        assetLatestPR = Asset.objects.filter(categoryName__icontains="printers").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestPR = None

    try:
        assetLatestCR = Asset.objects.filter(categoryName__icontains="cars").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestCR = None

    try:
        assetLatestTR = Asset.objects.filter(categoryName__icontains="trucks").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestTR = None

    try:
        assetLatestFT = Asset.objects.filter(categoryName__icontains="furniture").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestFT = None

    try:
        assetLatestLT = Asset.objects.filter(categoryName__icontains="laptops").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestLT = None

    try:
        assetLatestOTR = Asset.objects.filter(categoryName__icontains="others").latest('serialNumber')
    except Asset.DoesNotExist:
        assetLatestOTR = None

    #categories
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    var1 = None
    var2 = "No asset aded in this category"
    form = AssetModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        #form.instance.user = request.user
        form.save()
        return redirect('/thank-you/')

    context = {
        'form' : form,
        'var2' : var2,
        'assetLatestPR': assetLatestPR,
        'assetLatestCR': assetLatestCR,
        'assetLatestTR': assetLatestTR,
        'assetLatestFT': assetLatestFT,
        'assetLatestLT': assetLatestLT,
        'assetLatestOTR' : assetLatestOTR,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    
    return render(request, "register.html", context)

@login_required(login_url='../accounts/login/')
def category(request):
    form = CategoryModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        #form.instance.user = request.user
        form.save()
        return redirect('/dashboard/')
    context = {
        'form' : form
    }
    return render(request, "category_create.html", context)

@login_required(login_url='../accounts/login/')
def list_view_two(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.all().order_by('-serialNumber')
    assetTotal = Asset.objects.all()

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(categoryName__icontains=query)
                                | Q(serialNumber__icontains=query))
    
    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "dashboard.html", args)

@login_required(login_url='../accounts/login/')
def assets_worth(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")
    
    assets = Asset.objects.all().aggregate(Sum('purchasePrice'))['purchasePrice__sum'] or 0.00
    args = {
        'assets' : assets,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "reports/assets_worth.html", args)

@login_required(login_url='../accounts/login/')
def list_view_laptops(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="laptops").order_by('-serialNumber')
    assetTotal = Asset.objects.filter(categoryName__icontains="laptops")

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(categoryName__icontains=query)
                                | Q(serialNumber__icontains=query))
    
    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/laptops.html", args)

@login_required(login_url='../accounts/login/')
def list_view_cars(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="cars").order_by('-serialNumber')
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotalCars' : assetTotalCars,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/cars.html", args)

@login_required(login_url='../accounts/login/')
def list_view_printers(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="printers").order_by('-serialNumber')
    assetTotal = Asset.objects.filter(categoryName__icontains="printers")

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/printers.html", args)

@login_required(login_url='../accounts/login/')
def list_view_trucks(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="trucks").order_by('-serialNumber')
    assetTotal = Asset.objects.filter(categoryName__icontains="trucks")
    paginator = Paginator(assets, 25) # Show 25 contacts per page

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/trucks.html", args)

@login_required(login_url='../accounts/login/')
def list_view_furniture(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="furniture").order_by('-serialNumber')
    assetTotal = Asset.objects.filter(categoryName__icontains="furniture")

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/furniture.html", args)

@login_required(login_url='../accounts/login/')
def list_view_others(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(categoryName__icontains="others").order_by('-serialNumber')
    assetTotal = Asset.objects.filter(categoryName__icontains="others")

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/others.html", args)

@login_required(login_url='../accounts/login/')
def renting_module(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(rentStatus__isnull=False).order_by('-serialNumber')
    assetTotal = Asset.objects.filter(rentStatus__isnull=False)

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/rented_assets.html", args)

@login_required(login_url='../accounts/login/')
def movement_module(request):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")

    assets = Asset.objects.filter(assetMovement__icontains='yes').order_by('-serialNumber')
    assetTotal = Asset.objects.filter(assetMovement__icontains='yes')

    query = request.GET.get('q')
    if query:
        assets = assets.filter(Q(productName__icontains=query) | Q(serialNumber__icontains=query))

    paginator = Paginator(assets, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    args = {
        'assets' : assets,
        'assetTotal' : assetTotal,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return  render(request, "categories/assets_in_motion.html", args)


@login_required(login_url='../accounts/login/')
def asset_detail_view(request, id):
    assetTotalLaptops = Asset.objects.filter(categoryName__icontains="laptops")
    assetTotalPrinters = Asset.objects.filter(categoryName__icontains="printers")
    assetTotalFurniture = Asset.objects.filter(categoryName__icontains="furniture")
    assetTotalCars = Asset.objects.filter(categoryName__icontains="cars")
    assetTotalTrucks = Asset.objects.filter(categoryName__icontains="trucks")
    assetTotalOthers = Asset.objects.filter(categoryName__icontains="others")
    
    obj = get_object_or_404(Asset, id=id)
    context = { 
        'object' : obj,
        'assetTotalLaptops' : assetTotalLaptops,
        'assetTotalPrinters' : assetTotalPrinters,
        'assetTotalFurniture' : assetTotalFurniture,
        'assetTotalCars' : assetTotalCars,
        'assetTotalTrucks' : assetTotalTrucks,
        'assetTotalOthers' : assetTotalOthers
    }
    return render(request, "asset/detail.html", context)

class AssetDeleteView(DeleteView):
    template_name = 'asset/asset_delete.html'
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Asset, id=id_)

    def get_success_url(self):
        return reverse('dashboard')

class AssetUpdateView(UpdateView):
    template_name = 'asset/asset_update.html'
    form_class = AssetModelForm
    queryset = Asset.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Asset, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)