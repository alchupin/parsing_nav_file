from decimal import Decimal

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Min, Max
from django.core.exceptions import MultipleObjectsReturned

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


def parsing_nav_file(in_memory_file):
    """
    Извлекает необходимые данные из файла и сохраняет их во вновь созданных экземплярах модели NavData
    """
    GPRMC_all_list = []
    for line in in_memory_file:
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
                    altitude=Decimal(list_data[9])
                )
            elif line.startswith('$GPRMC'):
                GPRMC_all_list.append(line)
        except Exception as e:
            print(e)
    # Добавление значения скорости в созданные экземпляры модели
    for GPRMC_string in GPRMC_all_list:
        GPRMC_list = GPRMC_string.split(',')
        GPRMC_time_stamp = GPRMC_list[1].split('.')[0]
        if NavData.objects.filter(time_stamp=GPRMC_time_stamp).exists():
            try:
                nav_data = NavData.objects.get(time_stamp=GPRMC_time_stamp)
                nav_data.speed = Decimal(GPRMC_list[7])
                nav_data.save()
            except MultipleObjectsReturned:
                print('Данные занесены в базу')
    clean_nav_data()


def clean_nav_data():
    """
    Удаляет экземпляры модели NavData, поле "скорость" в которых не определено (None)
    """
    for nav_data in NavData.objects.all():
        if nav_data.speed is None:
            nav_data.delete()


def filter_qs(request):
    """
    Фильтрует данные в соответствии с пришедшими в GET-запросе параметрами высоты и скорости
    """
    qs = NavData.objects.all()
    altitude_min = request.GET.get('altitude_min')
    altitude_max = request.GET.get('altitude_max')
    speed_min = request.GET.get('speed_min')
    speed_max = request.GET.get('speed_max')

    if altitude_min is None or altitude_min == '':
        altitude_min = find_min_max('altitude')[0]
    if altitude_max is None or altitude_max == '':
        altitude_max = find_min_max('altitude')[1]
    if speed_min is None or speed_min == '':
        speed_min = find_min_max('speed')[0]
    if speed_max is None or speed_max == '':
        speed_max = find_min_max('speed')[1]

    qs = qs.filter(altitude__gte=altitude_min)
    qs = qs.filter(altitude__lte=altitude_max)
    qs = qs.filter(speed__gte=speed_min)
    qs = qs.filter(speed__lte=speed_max)
    return qs


def find_min_max(field_name):
    """
    Находит минимальное и максимальное значения заданного параметра
    для всех записей в БД и выводит их в виде кортежа значений
    """
    get_min = field_name + '__min'
    get_max = field_name + '__max'
    qs = NavData.objects.all()
    field_name_min = qs.aggregate(Min(field_name)).get(get_min)
    field_name_max = qs.aggregate(Max(field_name)).get(get_max)
    if field_name_min is None or field_name_min == '':
        field_name_min = 0
    if field_name_max is None or field_name_max == '':
        field_name_max = 0
    return float(field_name_min), float(field_name_max)


def display_results(request):
    """
    Передает данные (queryset, min и max значения высоты и скорости) для отображения в соответствующем шаблоне
    """
    qs = filter_qs(request)
    altitude_min, altitude_max = find_min_max('altitude')
    speed_min, speed_max = find_min_max('speed')
    context = {'qs': qs, 'al_min': altitude_min, 'al_max': altitude_max, 'speed_min': speed_min, 'speed_max': speed_max}
    return render(request, "parsing/results.html", context)
