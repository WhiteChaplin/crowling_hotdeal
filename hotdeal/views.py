from django.shortcuts import render
from .models import Deal
from rest_framework import viewsets
from .serializers import DealSerializers
from django.core.paginator import Paginator
# Create your views here.

sort_dict = {
    "정렬 기준(설정안함)":"",
    "1":"upload_date",
    "2":"-upload_date",
    "3":"price",
    "4":"-price",
}

category_dict = {
    "카테고리 선택(설정안함)":"",
    "1":"IT",
    "2":"상품권",
    "3":"가전/가구",
    "4":"생활/식품",
    "5":"의류/잡화/서적",
    "6":"기타 ",
    "7":"화장품"
}

def index(requests):
    deals = Deal.objects.all().order_by("upload_date")
    return render(requests,"index.html",{"deals":deals})

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializers
    
def test(requests):
    page = requests.GET.get('page','1')
    # print(requests.POST.get("sort-select"))
    print(requests.GET.get("sort-select"))
    print(requests.GET.get("sort-category"))
    print(requests.GET.get("search-keyword"))
    sort_select = requests.GET.get("sort-select")
    sort_category = requests.GET.get("sort-category")
    search_keyword = requests.GET.get("search-keyword")
    
    # deals = Deal.objects.filter(title__contains=search_keyword).order_by(sort_dict[sort_select])
    # print(sort_category)
    deals = Deal.objects.filter(title__contains=search_keyword)
    # deals.count()
    if category_dict[sort_category] != "":
        deals = deals.filter(category__contains = category_dict[sort_category])
    if sort_dict[sort_select] != "":
        deals = deals.order_by(sort_dict[sort_select])
    # print(deals.count()) #몇개 값 가져왔는지 확인 코드
    paginator = Paginator(deals,12)
    deal = paginator.get_page(page)
    return render(requests,"view.html",{"deals":deal, "setting":[search_keyword,sort_category,sort_select]})