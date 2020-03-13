from django.shortcuts import render, redirect
from .models import Events, query_event, Purchase, Chosen_event, query_last_price_event
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .top_documents import Top_documents


# Create your views here.
def homepage(request):
    event = request.GET.get("event")
    if not event:
        return render(request=request, template_name='main/home.html', context={'event': query_event()})
    return render(request=request, template_name='main/home.html', context={'event': query_event(event)})


def buy_tickets(request):
    return render(request=request, template_name='main/buy_tickets.html', context={'events': Events().get_events()})


def passed_events(request):
    return render(request=request, template_name='main/past_events.html', context={'events': Events().get_passed_events()})


def my_tickets(request):
    bought_tickets = []

    user = str(request.user)
    for item in Purchase.objects.all():
        if item.user == user:
            item.current_price = query_last_price_event(item.event.replace(" ", "_"))
            item.profit = (item.current_price - item.original_price) * item.nr_of_tickets_bought
            bought_tickets.append(item)

    return render(request=request, template_name='main/my_tickets.html', context={"my_events": bought_tickets})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = UserCreationForm
    return render(request=request, template_name="main/register.html", context={"form": form})


def buy(request):
    event = request.GET.get("event")
    if request.method == "POST":
        user = request.user
        event = request.POST.get("event")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        Purchase.objects.create(user= user, event=event, nr_of_tickets_bought=quantity, original_price=price)
        return redirect("main:my_tickets")
    return render(request=request, template_name='main/buy.html', context={'event': event})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"form": form})


def advicer(request):
    eventname = request.GET.get("event")
    event = Chosen_event(eventname)
    documents = event.get_documents(event)
    past_event = Top_documents(documents)
    return render(request=request, template_name='main/advice.html', context={'event': eventname,
                                                                              'time_highest_price': past_event.get_best_time_to_sell(),
                                                                              'price': past_event.get_highest_price(),
                                                                              'time_highest_supply_demand_ratio': past_event.get_time_highest_demand_to_supply_ratio(),
                                                                              'highest_increase_in_demand': past_event.get_time_highest_increase_in_searched_tickets(),
                                                                              'most_sold_in_an_hour': past_event.get_time_highest_sold_ratio()})