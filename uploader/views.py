import io
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile
import pandas as pd
import zipfile
from io import BytesIO


def process_file(file: UploadedFile):
    # Чтение содержимого файла
    raw_data = file.read().decode('utf-8')
    lines = raw_data.splitlines()  # Разделение на строки

    # Разделение строк на столбцы с использованием разделителя запятая
    data = [line.split(',') for line in lines]
    df = pd.DataFrame(data[1:], columns=data[0])  # Первая строка - заголовок, остальные - данные

    # Убедимся, что "Значение" является числовым столбцом
    df['Значение'] = pd.to_numeric(df['Значение'], errors='coerce')

    # Удаляем строки с некорректными данными (где Значение NaN)
    df = df.dropna(subset=['Начальное время', 'Значение'])

    # Создание первого файла в требуемом формате
    output1 = io.StringIO()
    df.to_csv(output1, index=False, sep=';')
    output1.seek(0)

    # Рассчитываем среднее значение за день
    daily_avg = df.copy()
    daily_avg['Дата'] = pd.to_datetime(df['Начальное время']).dt.date
    daily_avg = daily_avg.groupby('Дата', as_index=False)['Значение'].mean()
    daily_avg['Значение'] = daily_avg['Значение'].round(2)
    daily_avg.rename(columns={'Значение': 'Среднее значение'}, inplace=True)

    # Создание второго файла со средними значениями за день
    output2 = io.StringIO()
    daily_avg.to_csv(output2, index=False, sep=';')
    output2.seek(0)

    # Возврат обоих файлов
    return {
        "file1": io.BytesIO(output1.getvalue().encode('utf-8')),
        "file2": io.BytesIO(output2.getvalue().encode('utf-8')),
    }


def file_view(request):
    error_message = None

    if request.method == "POST":
        file = request.FILES.get('file')
        action = request.POST.get('action')  # Получаем действие (file1 или file2)

        if not file:
            error_message = "Файл не был загружен. Пожалуйста, загрузите файл."
        elif not file.name.endswith('.csv'):
            error_message = "Недопустимый формат файла. Загрузите файл в формате CSV."
        else:
            try:
                processed_files = process_file(file)

                # В зависимости от действия возвращаем нужный файл
                if action == "file1":
                    response = HttpResponse(
                        processed_files["file1"],
                        content_type='text/csv',
                    )
                    response['Content-Disposition'] = f'attachment; filename="processed_{file.name}"'
                    return response
                elif action == "file2":
                    response = HttpResponse(
                        processed_files["file2"],
                        content_type='text/csv',
                    )
                    response['Content-Disposition'] = f'attachment; filename="daily_avg_{file.name}"'
                    return response

            except Exception as e:
                error_message = f"Произошла ошибка при обработке файла: {str(e)}"

    return render(request, 'upload.html', {'error_message': error_message})
