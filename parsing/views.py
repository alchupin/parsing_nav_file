from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Min, Max

from .forms import UploadFileForm
from .models import NavData


def upload(request):
    """
    Загружает файл с помощью формы
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            parsing_nav_file(request.FILES['file'])
            return HttpResponseRedirect('/results/')
        return render(request, 'parsing/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'parsing/upload.html', {'form': form})


def parsing_nav_file(file):
    """
    Извлекает необходимые данные из файла и сохраняет их во вновь созданных экземплярах модели
    """
    for line in file.readlines():
        try:
            line = line.decode('ascii')
            if line.startswith('$GPGGA'):
                list_data = line.split(',')
                nd = NavData.objects.create(
                    time_stamp=list_data[1].split('.')[0],
                    latitude_degrees=list_data[2][:2],
                    latitude_minutes=list_data[2][2:],
                    latitude_dir=list_data[3],
                    longitude_degrees=list_data[4][:2],
                    longitude_minutes=list_data[4][2:],
                    longitude_dir=list_data[5],
                    altitude=list_data[9]
                )
        except Exception as e:
            print(e)


def filter_qs(request):
    """
    Фильтрует данные в соответствии с пришедшими в GET-запросе параметрами
    """
    qs = NavData.objects.all()
    altitude_min = request.GET.get('altitude_min')
    altitude_max = request.GET.get('altitude_max')
    if altitude_min is None or altitude_min == '':
        altitude_min = find_min_max()[0]
    if altitude_max is None or altitude_max == '':
        altitude_max = find_min_max()[1]
    qs = qs.filter(altitude__gte=altitude_min)
    qs = qs.filter(altitude__lte=altitude_max)
    return qs


def find_min_max():
    """
    Находит минимальное и максимальное значения высоты для всех записей в БД и выводит их в виде кортежа значений
    """
    qs = NavData.objects.all()
    altitude_min = qs.aggregate(Min('altitude')).get('altitude__min')
    altitude_max = qs.aggregate(Max('altitude')).get('altitude__max')
    if altitude_min is None or altitude_min == '':
        altitude_min = 0
    if altitude_max is None or altitude_max == '':
        altitude_max = 0
    return altitude_min, altitude_max


def display_results(request):
    """
    Передает данные (queryset, min и max значения высоты) для отображения в соответствующем шаблоне
    """
    qs = filter_qs(request)
    altitude_min, altitude_max = find_min_max()
    context = {'qs': qs, 'al_min': altitude_min, 'al_max': altitude_max}
    return render(request, "parsing/results.html", context)
