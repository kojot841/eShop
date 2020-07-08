from django.shortcuts import render
from .forms import ReceptForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from .models import Recept
from django.contrib.auth.models import User
# Create your views here.

class HomeView(TemplateView):
    template_name = 'recepti/recepti.html'

    def get(self, request):
        form = ReceptForm()
        posts = Recept.objects.all().order_by('-kreirano')
        users = User.objects.exclude(id=request.user.id)
        context = {'form':form, 'posts':posts, 'users': users,}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ReceptForm(request.POST, None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save() #ova i dve linije iznad je kako se cuvaju objekti u djangu u bazi podataka na osnovu base model form
            text = form.cleaned_data['post']
            form = ReceptForm()
            return redirect('recepti')
        context = {'form':form, 'text': text,}
        return render(request, self.template_name, context)


class PretragaRecepti(ListView):
    template_name = 'recepti/pretraga-recepti.html'

    def get_queryset(self, *args, **kwargs):
        request     = self.request
        query       = request.GET.get('q')
        if query is not None:
            lookups = Q(post__icontains=query)
            return Recept.objects.filter(lookups)
        return Recept.objects.none().distinct()