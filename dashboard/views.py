import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import Result
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Dataset, Relevant, Categorical
from .forms import CSVUploadForm
from django.core.paginator import Paginator
import os
from django.conf import settings
import io
import base64
from django.db.models import Count
import ktrain
from ktrain import text
import random
from django.db.models import Count, Q  # Import Count and Q


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def source_list(request):
    sources = Dataset.objects.all().values('id', 'text', 'username', 'date')
    paginator = Paginator(sources, 5)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_sources = paginator.get_page(page_number)
    return render(request, 'source_list.html', {'sources': page_sources})


def process_selected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_rows')
        selected_rows = Dataset.objects.filter(id__in=selected_ids)
        for row in selected_rows:
            prediction_value = random.choice([True, False])
            if prediction_value:
                prediction_value = 1
            else:
                prediction_value = 0
            print(prediction_value)

            new_result = Result(
                id=row.id,
                text=row.text,
                output=prediction_value,
                username=row.username,
                date=row.date)
            new_result.save()
            new_result.update_user_count()

            # Query data from the database
        results = Result.objects.all()
        # Count the number of 'Yes' and 'No' outputs
        num_yes = results.filter(output=True).count()
        num_no = results.filter(output=False).count()

        # Retrieve dates from the Result model and store them in a list
        dates_list = Result.objects.values_list('date', flat=True).distinct()

        # Convert the dates_list queryset to a Python list
        dates_list = [str(date) for date in dates_list]

        # print(dates_list)

        # Retrieve dates from the Result model and store them in a list
        dates_list_1 = Result.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of False values in the output field for each date
        false_counts_by_date = Result.objects.filter(output=False).values('date').annotate(false_count=Count('output'))

        # Create a dictionary to store the results
        false_counts_dict = {entry['date']: entry['false_count'] for entry in false_counts_by_date}

        # Create a list of false counts that matches the dates in the date list
        numSpam_list = [false_counts_dict.get(date, 0) for date in dates_list_1]

        # print(numSpam_list)

        # Retrieve dates from the Result model and store them in a list
        dates_list_2 = Result.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of True values in the output field for each date
        true_counts_by_date = Result.objects.filter(output=True).values('date').annotate(true_count=Count('output'))

        # Create a dictionary to store the results
        true_counts_dict = {entry['date']: entry['true_count'] for entry in true_counts_by_date}

        # Create a list of true counts that matches the dates in the date list
        numNotSpam_list = [true_counts_dict.get(date, 0) for date in dates_list_2]

        # print(numNotSpam_list)

        # get spam and not spam
        # Count the number of 'Yes' and 'No' outputs
        not_spam_data = results.filter(output=True)
        spam_data = results.filter(output=False)

        # Pagination
        page_number = request.GET.get('page')
        paginator = Paginator(spam_data, 5)  # Display 10 items per page
        page_obj = paginator.get_page(page_number)

        # Pagination1
        page_number1 = request.GET.get('page1')
        paginator = Paginator(not_spam_data, 5)  # Display 10 items per page
        page_obj_1 = paginator.get_page(page_number1)
        # Get the number of users with user count greater than ten
        num_users_greater_than_ten = Result.objects.filter(user_count__gt=10).values('username').distinct().count()

        # Get the number of users with user count less than or equal to ten
        num_users_smaller_than_ten = Result.objects.filter(user_count__lte=10).values('username').distinct().count()

        # Get the number of users with user count equals zero
        num_users_of_zero_relevant = Result.objects.filter(user_count=0).values('username').distinct().count()

        # Query to get user stats
        user_stats = Result.objects.values('username').annotate(
            spam=Count('output', filter=Q(output=False)),
            not_spam=Count('output', filter=Q(output=True)),
            total=Count('output', filter=Q(output=False)) + Count('output', filter=Q(output=True))
        )

        # Create a list of objects with user stats
        user_stats_list = []
        for stat in user_stats:
            user_stat_obj = {
                'user': stat['username'],
                'spam': stat['spam'],
                'not_spam': stat['not_spam'],
                'total': stat['total']
            }
            user_stats_list.append(user_stat_obj)

        print(user_stats_list)

        # Pagination2
        page_number2 = request.GET.get('page2')
        paginator = Paginator(user_stats_list, 5)  # Display 10 items per page
        page_obj_2 = paginator.get_page(page_number2)

        return render(request, 'dashboard_spam.html',
                      {
                          'num_yes': num_yes,
                          'num_no': num_no,
                          'num_greater_than_ten': num_users_greater_than_ten,
                          'num_smaller_than_ten': num_users_smaller_than_ten,
                          'num_of_zero_spam': num_users_of_zero_relevant,
                          'date_lists': dates_list,
                          'numSpam_list': numSpam_list,
                          'numNotSpam_list': numNotSpam_list,
                          'page_obj': page_obj,
                          'page_obj_1': page_obj_1,
                          'page_obj_2': page_obj_2
                      })
    # Handle the case when the request method is not POST
    # You might want to redirect or return an appropriate response here
    return HttpResponse("Invalid request method")


def process_relevant_source(request):
    true_results = Result.objects.filter(output=True)
    # Pagination
    paginator = Paginator(true_results, 5)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'relevant_source.html', {'page_obj': page_obj})


def process_relevant_selected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_rows')

        print("herrrrrrrrrrrrrrrrrrrrrrrrrr")
        print(selected_ids)

        # Now you have the list of selected IDs, you can retrieve the corresponding Result objects
        selected_results = Result.objects.filter(id__in=selected_ids)

        for row in selected_results:
            prediction_value = random.choice([True, False])
            if prediction_value:
                prediction_value = 1
            else:
                prediction_value = 0
            print(prediction_value)

            new_obj = Relevant(
                id=row.id,
                text=row.text,
                spam=row.output,
                relevant=prediction_value,
                username=row.username,
                date=row.date)
            new_obj.save()
            new_obj.update_user_count()

            # Query data from the relevant table
        results = Relevant.objects.all()
        # Count the number of 'Yes' and 'No' outputs
        num_yes = results.filter(relevant=True).count()
        num_no = results.filter(relevant=False).count()

        # Retrieve dates from the Relevant model and store them in a list
        dates_list = Relevant.objects.values_list('date', flat=True).distinct()

        # Convert the dates_list queryset to a Python list
        dates_list = [str(date) for date in dates_list]

        # print(dates_list)

        # Retrieve dates from the Relevant model and store them in a list
        dates_list_1 = Relevant.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of False values in the relevant field for each date
        false_counts_by_date = Relevant.objects.filter(relevant=False).values('date').annotate(
            false_count=Count('relevant'))

        # Create a dictionary to store the results
        false_counts_dict = {entry['date']: entry['false_count'] for entry in false_counts_by_date}

        # Create a list of false counts that matches the dates in the date list
        num_relevant_list = [false_counts_dict.get(date, 0) for date in dates_list_1]

        print(num_relevant_list)

        # Retrieve dates from the Relevant model and store them in a list
        dates_list_2 = Relevant.objects.values_list('date', flat=True).distinct()

        # Aggregate the number of True values in the relevant field for each date
        true_counts_by_date = Relevant.objects.filter(relevant=True).values('date').annotate(
            true_count=Count('relevant'))

        # Create a dictionary to store the results
        true_counts_dict = {entry['date']: entry['true_count'] for entry in true_counts_by_date}

        # Create a list of true counts that matches the dates in the date list
        num_not_relevant_list = [true_counts_dict.get(date, 0) for date in dates_list_2]

        print(num_not_relevant_list)

        # get relevant and not relevant
        # Count the number of 'Yes' and 'No' relevant
        not_relevant_data = results.filter(relevant=True)
        relevant_data = results.filter(relevant=False)

        # Pagination
        page_number = request.GET.get('page')
        paginator = Paginator(relevant_data, 5)  # Display 10 items per page
        page_obj = paginator.get_page(page_number)

        # Pagination1
        page_number1 = request.GET.get('page1')
        paginator = Paginator(not_relevant_data, 5)  # Display 10 items per page
        page_obj_1 = paginator.get_page(page_number1)

        # Get the number of users with user count greater than ten
        num_users_greater_than_ten = Relevant.objects.filter(user_count__gt=10).values('username').distinct().count()

        # Get the number of users with user count less than or equal to ten
        num_users_smaller_than_ten = Relevant.objects.filter(user_count__lte=10).values('username').distinct().count()

        # Get the number of users with user count equals zero
        num_users_of_zero_relevant = Relevant.objects.filter(user_count=0).values('username').distinct().count()


        # Query to get user stats
        user_stats = Relevant.objects.values('username').annotate(
            relevant_s=Count('relevant', filter=Q(relevant=False)),
            not_relevant_s=Count('relevant', filter=Q(relevant=True)),
            total=Count('relevant', filter=Q(relevant=False)) + Count('relevant', filter=Q(relevant=True))
        )

        # Create a list of objects with user stats
        user_stats_list = []
        for stat in user_stats:
            user_stat_obj = {
                'user': stat['username'],
                'relevant': stat['relevant_s'],
                'not_relevant': stat['not_relevant_s'],
                'total': stat['total']
            }
            user_stats_list.append(user_stat_obj)

        print(user_stats_list)

        # Pagination2
        page_number2 = request.GET.get('page2')
        paginator = Paginator(user_stats_list, 5)  # Display 10 items per page
        page_obj_2 = paginator.get_page(page_number2)

        return render(request, 'dashboard_relevant.html',
                      {
                          'num_yes': num_yes,
                          'num_no': num_no,
                          'num_greater_than_ten': num_users_greater_than_ten,
                          'num_smaller_than_ten': num_users_smaller_than_ten,
                          'num_of_zero_relevant': num_users_of_zero_relevant,
                          'date_lists': dates_list,
                          'num_relevant_list': num_relevant_list,
                          'num_not_relevant_list': num_not_relevant_list,
                          'page_obj': page_obj,
                          'page_obj_1': page_obj_1,
                          'page_obj_2': page_obj_2
                      })
    # Handle the case when the request method is not POST
    # You might want to redirect or return an appropriate response here
    return HttpResponse("Invalid request method")


def categorical_relevant_dashboard(request):
    selected_rows = request.GET.get('selected_rows')  # Retrieve selected IDs from query parameters

    # Convert the selected IDs into a list
    selected_ids = selected_rows.split(",") if selected_rows else []

    # Query the selected rows from the Relevant table based on the IDs
    selected_relevant_results = Relevant.objects.filter(id__in=selected_ids)

    print(selected_relevant_results)

    numbers = [1, 2, 3]
    # Now you have the list of selected IDs, you can retrieve the corresponding Result objects
    selected_results = Relevant.objects.filter(id__in=selected_ids)

    for row in selected_results:
        prediction_value = random.choice(numbers)
        print(prediction_value)
        new_obj = Categorical(
            id=row.id,
            text=row.text,
            category=prediction_value,
            username=row.username,
            date=row.date)
        new_obj.save()

        # Query data from the Categorical table
    results = Categorical.objects.all()
    # Count the number of '1' and '2' and '3' predictions
    num_of_1 = results.filter(category=1).count()
    num_of_2 = results.filter(category=2).count()
    num_of_3 = results.filter(category=3).count()

    # Retrieve dates from the Relevant model and store them in a list
    dates_list = Categorical.objects.values_list('date', flat=True).distinct()

    # Convert the dates_list queryset to a Python list
    dates_list = [str(date) for date in dates_list]

    # print(dates_list)

    # Retrieve dates from the Relevant model and store them in a list
    dates_list_1 = Categorical.objects.values_list('date', flat=True).distinct()

    # Aggregate the number of False values in the relevant field for each date
    ones_counts_by_date = Categorical.objects.filter(category=1).values('date').annotate(ones_count=Count('category'))

    # Create a dictionary to store the results
    ones_counts_dict = {entry['date']: entry['ones_count'] for entry in ones_counts_by_date}

    # Create a list of ones counts that matches the dates in the date list
    num_ones_list = [ones_counts_dict.get(date, 0) for date in dates_list_1]

    print("here are the ones list")
    print(num_ones_list)

    # Retrieve dates from the Categorical model and store them in a list
    dates_list_2 = Categorical.objects.values_list('date', flat=True).distinct()

    # Aggregate the number of True values in the Categorical field for each date
    twos_counts_by_date = Categorical.objects.filter(category=2).values('date').annotate(twos_count=Count('category'))

    # Create a dictionary to store the results
    twos_counts_dict = {entry['date']: entry['twos_count'] for entry in twos_counts_by_date}

    # Create a list of true counts that matches the dates in the date list
    num_twos_list = [twos_counts_dict.get(date, 0) for date in dates_list_2]

    # threes
    # Retrieve dates from the Categorical model and store them in a list
    dates_list_3 = Categorical.objects.values_list('date', flat=True).distinct()

    # Aggregate the number of True values in the Categorical field for each date
    threes_counts_by_date = Categorical.objects.filter(category=3).values('date').annotate(threes_count=Count('category'))

    # Create a dictionary to store the results
    threes_counts_dict = {entry['date']: entry['threes_count'] for entry in threes_counts_by_date}

    # Create a list of true counts that matches the dates in the date list
    num_threes_list = [threes_counts_dict.get(date, 0) for date in dates_list_3]

    # get every one
    ones_data = results.filter(category=1)
    twos_data = results.filter(category=2)
    threes_data = results.filter(category=3)

    data_all = Categorical.objects.all();

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(data_all, 5)  # Display 10 items per page
    page_obj = paginator.get_page(page_number)

    print(num_of_1)
    print(num_of_2)
    print(num_of_3)
    print(num_ones_list)
    print(num_twos_list)
    print(num_threes_list)
    print(dates_list)

    return render(request, 'categorical.html',
                  {
                      'num_of_1': num_of_1,
                      'num_of_2': num_of_2,
                      'num_of_3': num_of_3,
                      'date_lists': dates_list,
                      'num_ones_list': num_ones_list,
                      'num_twos_list': num_twos_list,
                      'num_threes_list': num_threes_list,
                      'page_obj': page_obj,
                  })

