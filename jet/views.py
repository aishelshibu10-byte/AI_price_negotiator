from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jet.models import Product, CartItem, CustomerProfile
from jet.negotiation_engine import evaluate_offer, MAX_ROUNDS
from jet.gemini_responder import generate_negotiation_reply
from django.contrib.auth.decorators import user_passes_test
from jet.ml.negotiator import predict_min_price
from django.db.models import Count, Sum as DjangoSum


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
        action = request.POST.get('action')

        if action == 'reset_negotiation':
            if session_key in request.session:
                del request.session[session_key]
            return redirect('product_detail', pk=pk)

        if action == 'add_original':
            item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'agreed_price': product.original_price, 'negotiated': False, 'quantity': 1}
            )
            if not created:
                item.quantity += 1
                item.save()
            messages.success(request, f"{product.name} added to cart at ₹{item.agreed_price} each.")
            return redirect('product_detail', pk=pk)

        if action == 'add_negotiated':
            if negotiation.get("ended") and negotiation.get("decision") == "ACCEPT":
                item, created = CartItem.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'agreed_price': negotiation["final_price"], 'negotiated': True, 'quantity': 1}
                )
                if not created:
                    item.quantity += 1
                    item.save()
                del request.session[session_key]
                messages.success(request, f"{product.name} added to cart at ₹{item.agreed_price} each (negotiated).")
                return redirect('product_detail', pk=pk)
            else:
                messages.error(request, "You need to complete a successful negotiation first.")
                return redirect('product_detail', pk=pk)

        # Otherwise, treat this as a negotiation offer submission
        try:
            customer_offer = float(request.POST.get('offer_price'))
        except (TypeError, ValueError):
            messages.error(request, "Please enter a valid offer amount.")
            return redirect('product_detail', pk=pk)

        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        segment = profile.segment
        current_round = negotiation.get("round", 1)

        result = evaluate_offer(product, segment, current_round, customer_offer)

        ai_message = generate_negotiation_reply(
            decision=result["decision"],
            product_name=product.name,
            customer_offer=result["customer_offer"],
            final_price=result.get("final_price"),
        )
        result["ai_message"] = ai_message

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


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in items)
    return render(request, 'jet/cart.html', {'items': items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')


@login_required
def checkout_view(request):
    items = CartItem.objects.filter(user=request.user)

    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    total = sum(item.subtotal for item in items)

    if request.method == 'POST':
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        profile.total_orders += 1
        profile.total_spent += total
        profile.update_segment()

        items.delete()

        messages.success(request, "Order placed successfully! (Demo payment)")
        return redirect('order_success')

    return render(request, 'jet/checkout.html', {'items': items, 'total': total})


@login_required
def order_success(request):
    return render(request, 'jet/order_success.html')


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


@user_passes_test(lambda u: u.is_superuser)
def debug_negotiation(request, pk):
    product = get_object_or_404(Product, pk=pk)
    segments = ["NEW", "RETURNING", "PREMIUM"]
    rounds = [1, 2, 3]

    predictions = []
    for seg in segments:
        for rnd in rounds:
            price = predict_min_price(product, seg, rnd)
            predictions.append({
                "segment": seg,
                "round": rnd,
                "predicted_min_price": round(price, 2),
            })

    context = {
        "product": product,
        "predictions": predictions,
    }
    return render(request, 'jet/debug_negotiation.html', context)




@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = CustomerProfile.objects.count()
    segment_counts = CustomerProfile.objects.values('segment').annotate(count=Count('id'))

    total_revenue = CustomerProfile.objects.aggregate(total=DjangoSum('total_spent'))['total'] or 0
    total_orders = CustomerProfile.objects.aggregate(total=DjangoSum('total_orders'))['total'] or 0

    top_customers = CustomerProfile.objects.order_by('-total_spent')[:5]

    context = {
        "total_users": total_users,
        "segment_counts": segment_counts,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "top_customers": top_customers,
    }
    return render(request, 'jet/admin_dashboard.html', context)