from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, Category
from .forms import AdForm


def home(request):
    """Главная страница - список объявлений с фильтром и поиском"""
    ads_list = Ad.objects.filter(status='active').select_related('author', 'category')
    
    # Фильтр по категории
    category_slug = request.GET.get('category')
    if category_slug:
        ads_list = ads_list.filter(category__slug=category_slug)
    
    # Поиск по заголовку и описанию
    search_query = request.GET.get('search')
    if search_query:
        ads_list = ads_list.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(ads_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'ads/home.html', context)


def ad_detail(request, pk):
    """Детальная страница объявления"""
    ad = get_object_or_404(Ad, pk=pk)
    
    # Увеличиваем счётчик просмотров
    ad.increment_views()
    
    context = {
        'ad': ad,
    }
    return render(request, 'ads/ad_detail.html', context)


@login_required
def ad_create(request):
    """Создание объявления (только для авторизованных)"""
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    
    context = {
        'form': form,
        'title': 'Создать объявление',
    }
    return render(request, 'ads/ad_form.html', context)


@login_required
def ad_edit(request, pk):
    """Редактирование объявления (только для автора)"""
    ad = get_object_or_404(Ad, pk=pk)
    
    # Проверка: только автор может редактировать
    if ad.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои объявления!')
        return redirect('ad_detail', pk=pk)
    
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    
    context = {
        'form': form,
        'title': 'Редактировать объявление',
        'ad': ad,
    }
    return render(request, 'ads/ad_form.html', context)


@login_required
def ad_delete(request, pk):
    """Удаление объявления (только для автора)"""
    ad = get_object_or_404(Ad, pk=pk)
    
    # Проверка: только автор может удалить
    if ad.author != request.user:
        messages.error(request, 'Вы можете удалять только свои объявления!')
        return redirect('ad_detail', pk=pk)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление успешно удалено!')
        return redirect('my_ads')
    
    context = {
        'ad': ad,
    }
    return render(request, 'ads/ad_confirm_delete.html', context)


@login_required
def my_ads(request):
    """Мои объявления"""
    ads_list = Ad.objects.filter(author=request.user).select_related('category')
    
    # Пагинация
    paginator = Paginator(ads_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'ads/my_ads.html', context)


@login_required
def ad_toggle_status(request, pk):
    """Переключение статуса объявления (активно/неактивно)"""
    ad = get_object_or_404(Ad, pk=pk)
    
    if ad.author != request.user:
        messages.error(request, 'Вы можете управлять только своими объявлениями!')
        return redirect('my_ads')
    
    ad.status = 'inactive' if ad.status == 'active' else 'active'
    ad.save()
    
    status_text = 'снято с публикации' if ad.status == 'inactive' else 'опубликовано'
    messages.success(request, f'Объявление {status_text}!')
    return redirect('my_ads')


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'ads/register.html', context)
