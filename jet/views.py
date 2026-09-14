from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jet.models import Product
from jet.negotiation_engine import evaluate_offer, MAX_ROUNDS


def product_list(request):
    products = Product.objects.all()
    return render(request, 'jet/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    session_key = f"negotiation_{pk}"
    negotiation = request.session.get(session_key, {"round": 1, "ended": False})

    result = None

    if request.method == 'POST':
        try:
            customer_offer = float(request.POST.get('offer_price'))
        except (TypeError, ValueError):
            messages.error(request, "Please enter a valid offer amount.")
            return redirect('product_detail', pk=pk)

        segment = getattr(request.user.profile, 'segment', 'NEW')
        current_round = negotiation.get("round", 1)

        result = evaluate_offer(product, segment, current_round, customer_offer)

        if result["decision"] == "ACCEPT" or current_round >= MAX_ROUNDS:
            negotiation["ended"] = True
            negotiation["final_price"] = result["final_price"]
            negotiation["decision"] = result["decision"]
        else:
            negotiation["round"] = current_round + 1

        request.session[session_key] = negotiation

    context = {
        "product": product,
        "negotiation": negotiation,
        "result": result,
        "max_rounds": MAX_ROUNDS,
    }
    return render(request, 'jet/product_detail.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'jet/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'jet/login.html')


def logout_view(request):
    logout(request)
    return redirect('product_list')