from django.shortcuts import render
from django.http import JsonResponse

from .service import search_company,get_stock_data,calculate_basic_statistics,calculate_moving_average

# Create your views here.
def home(request):
    return render(request,"Home.html")

def company_search(request):
    query = request.GET.get("q","").strip()

    if not query:
        return JsonResponse({"results":[]})

    try:
        results = search_company(query)

        return JsonResponse(
            {"results": results}
        )
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status = 500)

def stock_data(request):
    ticker = request.GET.get("ticker", "").strip()
    period = request.GET.get("period", "1y").strip()

    if not ticker:
        return JsonResponse({
            "error":"Ticker is required"
        },status = 400)

    try:
        data = get_stock_data(ticker,period)

        data = calculate_moving_average(data)

        statistics = calculate_basic_statistics(data)

        return JsonResponse({
            "ticker" : ticker,
            "period" : period,
            "statistics" : statistics,
            "data" : data.reset_index().to_dict(orient="records")
        })
    except Exception as e:
        return JsonResponse({
            "error" : str(e)
        }, status = 500)