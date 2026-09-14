from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import HousePredictionForm
from .services import predict_from_form


def home(request):
    form = HousePredictionForm(request.POST or None)
    prediction = None

    if request.method == "POST" and form.is_valid():
        prediction = predict_from_form(form)

    return render(
        request,
        "predictor/home.html",
        {"form": form, "prediction": prediction},
    )

@csrf_exempt
@require_POST
def predict_api(request):
    form = HousePredictionForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    prediction = predict_from_form(form)

    return JsonResponse(
        {
            "success": True,
            "predicted_price": round(prediction, 2),
        }
    )