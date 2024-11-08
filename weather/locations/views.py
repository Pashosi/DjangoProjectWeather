from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from locations.forms import SearchLocations


# Create your views here.
content = {'Москва': 'Показываю город'}

def weather_checker(request):
    form = SearchLocations(request.POST)
    if form.is_valid():
        print(form.cleaned_data)

    data = {
        'title': 'Страница поиска локаций',
        'form': form
    }
    return render(request, 'locations/index.html', context=data)



class WeatherChecker(FormView):
    template_name = 'locations/index.html'
    form_class = SearchLocations
    extra_context = {
        'title': 'Страница поиска локаций',
    }
    success_url = '/'

    def form_valid(self, form):
        city = form.cleaned_data['city']

        # добавление в сессию новый город
        cities = self.request.session.get('cities', [])
        cities.append(city)

        # обновление сессии
        self.request.session['cities'] = cities

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = self.request.session.get('cities', [])
        return context
    

