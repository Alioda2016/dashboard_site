import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import Result
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Dataset
from .forms import CSVUploadForm
from django.core.paginator import Paginator
import os
from django.conf import settings
import io
import base64
from django.db.models import Count


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def source_list(request):
    sources = Dataset.objects.all().values('text', 'username', 'date')
    paginator = Paginator(sources, 5)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_sources = paginator.get_page(page_number)
    return render(request, 'source_list.html', {'sources': page_sources})


def process_selected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_rows')
        selected_rows = Result.objects.filter(id__in=selected_ids)

        # Query data from the database
        results = Result.objects.all()
        # Count the number of 'Yes' and 'No' outputs
        num_yes = results.filter(output=True).count()
        num_no = results.filter(output=False).count()

        # Retrieve dates from the Result model and store them in a list
        dates_list = Result.objects.values_list('date', flat=True).distinct()

        # Convert the dates_list queryset to a Python list
        dates_list = [str(date) for date in dates_list]

        print(dates_list)

        # Retrieve dates from the Result model and store them in a list
        dates_list_1 = Result.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of False values in the output field for each date
        false_counts_by_date = Result.objects.filter(output=False).values('date').annotate(false_count=Count('output'))

        # Create a dictionary to store the results
        false_counts_dict = {entry['date']: entry['false_count'] for entry in false_counts_by_date}

        # Create a list of false counts that matches the dates in the date list
        numSpam_list = [false_counts_dict.get(date, 0) for date in dates_list_1]

        print(numSpam_list)

        # Retrieve dates from the Result model and store them in a list
        dates_list_2 = Result.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of True values in the output field for each date
        true_counts_by_date = Result.objects.filter(output=True).values('date').annotate(true_count=Count('output'))

        # Create a dictionary to store the results
        true_counts_dict = {entry['date']: entry['true_count'] for entry in true_counts_by_date}

        # Create a list of true counts that matches the dates in the date list
        numNotSpam_list = [true_counts_dict.get(date, 0) for date in dates_list_2]

        print(numNotSpam_list)

        # get spam and not spam
        # Count the number of 'Yes' and 'No' outputs
        spam_data = results.filter(output=True)
        not_spam_data = results.filter(output=False)

        # Pagination
        page_number = request.GET.get('page')
        paginator = Paginator(spam_data, 5)  # Display 10 items per page
        page_obj = paginator.get_page(page_number)

        # Pagination1
        page_number1 = request.GET.get('page1')
        paginator = Paginator(not_spam_data, 5)  # Display 10 items per page
        page_obj_1 = paginator.get_page(page_number1)

        return render(request, 'dashboard_spam.html',
                      {
                          'num_yes': num_yes,
                          'num_no': num_no,
                          'num_greater_than_ten': 120,
                          'num_smaller_than_ten': 250,
                          'num_of_zero_spam': 500,
                          'date_lists': dates_list,
                          'numSpam_list': numSpam_list,
                          'numNotSpam_list': numNotSpam_list,
                          'page_obj': page_obj,
                          'page_obj_1': page_obj_1,
                      })
    # Handle the case when the request method is not POST
    # You might want to redirect or return an appropriate response here
    return HttpResponse("Invalid request method")
