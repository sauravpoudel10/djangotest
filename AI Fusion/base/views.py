from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from django.urls import reverse_lazy
from googlesearch import search  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView ,DetailView ,CreateView ,UpdateView ,DeleteView
import re
from collections import Counter
import requests
from urllib.parse import urlparse
from collections import defaultdict
import datetime
from bs4 import BeautifulSoup
import time 
from googlesearch import search
from django.contrib import messages
import datetime
from google_trends import daily_trends
from pytrends.request import TrendReq
from django.conf import settings
# from rembg import remove








def home(request):
    return render(request, 'home.html')
   

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'account created for {username}! ')
            return redirect ('home')
    else:
       form = UserRegisterForm()
    content = {'form' : form}
    return render (request, 'register.html',content)


   
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_blogs = Blog.objects.filter(author=user)

    context = {
        'user': user,
        'user_blogs': user_blogs,
    }

    return render(request, 'profile.html', context)


















































def custom_error_handler(request, exception=None):
    return render(request, 'notfound.html', status=404)














####### Scholarship
######
#####
####
###
##
#
# scraper/views.py
# import requests

def scholarships_view(request):
    query = request.GET.get('query')
    links = []

    if query:
        # Create a list of 10 specific links with the user's input
        links = [
            f"https://www.example1.com/search/{query}",
            f"https://www.example2.com/search/{query}",
            f"https://www.example3.com/search/{query}",
            f"https://www.example4.com/search/{query}",
            f"https://www.example5.com/search/{query}",
            f"https://www.example6.com/search/{query}",
            f"https://www.example7.com/search/{query}",
            f"https://www.example8.com/search/{query}",
            f"https://www.example9.com/search/{query}",
            f"https://www.example10.com/search/{query}"
        ]

    return render(request, 'scholar.html', {'query': query, 'links': links})







#     url = f"https://www.niche.com/colleges/search/best-colleges/"



    # url = f"https://www.petersons.com/search/scholarship?awardtype=SCHOL&q=scholarship+for+{location}&studenttype=UG"


#     url = 'https://www.scholarships.com/search/?q={}&location={}'.format(subject, location)
#


































####### Ai website 
######
#####
####
###
##
#

def search_ai_websites(request):
    search_results = []

    if request.method == 'POST':
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        query = f" ' ai website of category:{category}  and sub-category:{sub_category} AI websites ' "
        search_results = list(search(query))[:10]

    return render(request, 'aiwebfind.html', {'search_results': search_results})










































####### Ai website 
######
#####
####
###
##
#
import os
from django.conf import settings
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta








@login_required
def process_video(video,request):
    yt = YouTube(video.url)
    # stream = yt.streams.get_highest_resolution()
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    stream.download(output_path='media/videos', filename=f"{video.title}.mp4")

    video_path = os.path.abspath(f'media/videos/{video.title}.mp4')

    clip_start =  120 
    clip_end = 180  
    media_root = settings.MEDIA_ROOT

    while clip_start < yt.length:
        clip_filename = f"{video.title}_{clip_start}-{clip_end}.mp4"
        clip_path = os.path.join(media_root, 'clips', clip_filename)

        # clip_path = os.path.abspath(f'media/clips/{video.title}_{clip_start}-{clip_end}.mp4')

        ffmpeg_extract_subclip(video_path, clip_start, clip_end, targetname=clip_path)

        # Create a VideoClip object and set the user using the request.user
        clip = VideoClip.objects.create(
            video=video,
            clip=clip_path,
            start_time=clip_start,
            end_time=clip_end,
            user=request.user  # Set the user for the VideoClip
        )

        clip_start += 300
        clip_end = min(clip_start + 60, yt.length)

    os.remove(video_path)


@login_required
def index(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user  # Associate the video with the currently logged-in user
            video.save()
            process_video(video, request)
            return redirect('test')
    else:
        form = VideoForm()

    # Filter videos by the current user through the related VideoClip model
    video_ids = VideoClip.objects.filter(user=request.user).values_list('video_id', flat=True)
    videos = Video.objects.filter(id__in=video_ids)
    # recent_video = Video.objects.filter(user=request.user).order_by('-upload_date').first()

    if 'video_id' in request.GET:
        video_id = int(request.GET['video_id'])
        clips = VideoClip.objects.filter(video_id=video_id)
        
        return render(request, 'testing.html', {'form': form, 'videos': videos, 'clips': clips})

    return render(request, 'testing.html', {'form': form, 'videos': videos})



    # while clip_start < yt.length:
    #     clip_path = os.path.abspath(f'media/clips/{video.title}_{clip_start}-{clip_end}.mp4')

    #     ffmpeg_extract_subclip(video_path, clip_start, clip_end, targetname=clip_path)
    #     # ffmpeg_extract_subclip(video_path, clip_start, clip_end, targetname=clip_path, codec="aac", bitrate="192k")

    #     # VideoClip.objects.create(video=video, clip=clip_path, start_time=clip_start, end_time=clip_end)
    #     VideoClip.objects.create(video=video, clip=clip_path, start_time=clip_start, end_time=clip_end, user=request.user)

    #     clip_start += 300  # Move forward by 5 minutes (300 seconds)
    #     clip_end = min(clip_start + 60, yt.length)  # 1 minute clips, or until the end of the video

    # os.remove(video_path)  # Remove the original video

    # fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
    # VideoClip.objects.filter(video=video, user=request.user, upload_date__lt=fifteen_minutes_ago).delete()

    # fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
    # VideoClip.objects.filter(video=video, upload_date__lt=fifteen_minutes_ago).delete()















































# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
















def calculate_growth(request):
    if request.method == 'POST':
        # Get form data
        current_revenue = float(request.POST.get('current_revenue'))
        target_revenue = float(request.POST.get('target_revenue'))
        current_sales = int(request.POST.get('current_sales'))

        rent_percent = float(request.POST.get('rent_percent'))
        employee_percent = float(request.POST.get('employee_percent'))
        insurance_percent = float(request.POST.get('insurance_percent'))
        marketing_percent = float(request.POST.get('marketing_percent'))
        product_cost_percent = float(request.POST.get('product_cost_percent'))
        business_type = request.POST.get('business_type')

        # Calculate growth in sales
        growth_sales = target_revenue / (current_revenue / current_sales)

        # Check for rent warning
        rent_warning = rent_percent > 5

        # Render the results
        return render(request, 'business_revenue2.html', {
            'current_revenue': current_revenue,
            'target_revenue': target_revenue,
            'current_sales': current_sales,
            'growth_sales': growth_sales,
            'rent_warning': rent_warning,
            'business_type': business_type,
        })

    return render(request, 'business_revenue1.html')




# def find_growth(request):
#     if request.method == 'POST':
#         product_type = request.POST.get('product_type')
#         product_description = request.POST.get('product_description')
#         country = request.POST.get('country')

#         # Use the get_product_information function to get data
#         product_info = get_product_information(product_description, country)

#         # Render the results
#         return render(request, 'business_revenue3.html', {
       
#             'product_type': product_type,
#             'product_description': product_description,
#             'country': country,
#             'product_info': product_info,
#         })

#     return render(request, 'business_revenue2.html')





# calculator/utils.py
import requests
import json
from pytrends.exceptions import ResponseError


def get_product_information(product_description, country):

    trending_places = []

    query = f"regions in {country} where  {product_description} is more popular "
    trending_places = list(search(query))[:10]



    manufacturing_plants = []

    query = f"provide official company website   ' main manufacturer of {product_description} in {country} ' "
    manufacturing_plants = list(search(query))[:10]

    suppliers = []
    query = f" ' main suppliers of {product_description} in {country} ' "
    suppliers = list(search(query))[:10]

    return {
        'trending_places': [trending_place["geoName"] for trending_place in trending_places],
        'manufacturing_plants': [manufacturing_plant["name"] for manufacturing_plant in manufacturing_plants],
        'suppliers': [supplier["title"] for supplier in suppliers],
    }



# def get_product_information(product_description, country):
#     pytrends = pytrends.TrendReq()

#     pytrends.build_payload(
#     q=product_description,
#     geo=country,
#     timeframe="today"
# )

#     trending_places = pytrends.interest_by_region()[0][:50]
#     # # Get the top 20 manufacturing plants.
#     # manufacturing_plants = maps_api_data["results"][0:20]

#     manufacturing_plants = []

#     query = f"provide official company website   ' main manufacturer of {product_description} in {country} ' "
#     manufacturing_plants = list(search(query))[:20]

#     suppliers = []
#     # product = product_description
#     # place = country
#     query = f" ' main suppliers of {product_description} in {country} ' "
#     suppliers = list(search(query))[:20]

# # email find
# # https://hunter.io/try/search/pythonanywhere.eu?locale=en
#     return {
#         'trending_places': [trending_place["geoName"] for trending_place in trending_places],
#         'manufacturing_plants': [manufacturing_plant["name"] for manufacturing_plant in manufacturing_plants],
#         'suppliers': [supplier["title"] for supplier in suppliers],
#     }

# lix it tools 



def find_growth_business(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        product_description = request.POST.get('product_description')
        country = request.POST.get('country')

        # Use the get_product_information function to get data
        product_info = get_product_information(product_description, country)

        # Additional information for digital products
        if product_type == 'digital':
            seo_topics = ['SEO Basics', 'Keyword Research', 'On-Page SEO', 'Off-Page SEO']
            tv_shows = ['Show1', 'Show2', 'Show3']  # Add actual popular TV shows
            advertising_platforms = ['TikTok', 'Facebook', 'YouTube', 'Google Ads', 'Instagram', 'Twitter']

            # Render the results for digital products
            return render(request, 'business_revenue3.html', {
                'product_type': product_type,
                'product_description': product_description,
                'country': country,
                'product_info': product_info,
                'seo_topics': seo_topics,
                'tv_shows': tv_shows,
                'advertising_platforms': advertising_platforms,
            })

        # Render the results for other product types
        return render(request, 'business_revenue3.html', {
            'product_type': product_type,
            'product_description': product_description,
            'country': country,
            'product_info': product_info,
        })

    return render(request, 'business_revenue2.html')


def scrape_website(domain):
    url = f'http://{domain}'  # Assuming http for simplicity
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract emails using a simple regex
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)

        # Extract phone numbers with 10 digits or more
        phone_numbers = re.findall(r'\b\d{10,}\b', response.text)

        # Combine phone numbers into a string for simplicity
        contacts = '\n'.join(phone_numbers)

        return emails, contacts
    else:
        return None, None

def email_find(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        if domain:
            emails, contacts = scrape_website(domain)
            return render(request, 'business_email.html', {'emails': emails, 'contacts': contacts})

    return render(request, 'business_email.html')
































from math import log

def finance_calculator(request):
    result = None
    home_loan_warning = None
    expenses_warning = None
    goal_results = {}

    if request.method == 'POST':
        income = float(request.POST.get('income'))
        home_loan_emi = float(request.POST.get('home_loan_emi'))
        car_loan_emi = float(request.POST.get('car_loan_emi'))
        expenses = float(request.POST.get('expenses'))
        goal_amount = float(request.POST.get('goal_amount'))

        total_expenses = home_loan_emi + car_loan_emi + expenses

        if (home_loan_emi + car_loan_emi) > 0.3 * income:
            home_loan_warning = "Warning: Home loan and car loan EMI exceed 30% of income."

        if total_expenses > 0.7 * income:
            expenses_warning = "Warning: Total expenses exceed 70% of income."
        


        monthly_investment_percentages = [0.1, 0.2, 0.3, 0.4]  # 10%, 20%, 30%, 40% of monthly income
        yearly_compounding_rate = 0.12  # 12% annual compounding rate
        monthly_rate = 0.01 # Monthly rate

        monthly_income = income  # Assuming income is monthly

        goal_results = {}

        for percentage in monthly_investment_percentages:
            time_months = log(1 + (goal_amount / (percentage * monthly_income) - 1) / (1 + monthly_rate)) / log(1 + monthly_rate)
            time_years = round(time_months / 12, 2)  # Convert months to years
            goal_results[percentage] = time_years

    return render(request, 'finance_calculator.html', {'result': result, 'home_loan_warning': home_loan_warning, 'expenses_warning': expenses_warning, 'goal_results': goal_results})


# def finance_calculator(request):
#     result = None
#     home_loan_warning = None
#     expenses_warning = None

#     if request.method == 'POST':
#         income = float(request.POST.get('income'))
#         home_loan_emi = float(request.POST.get('home_loan_emi'))
#         car_loan_emi = float(request.POST.get('car_loan_emi'))
#         expenses = float(request.POST.get('expenses'))
#         goal_amount = float(request.POST.get('goal_amount'))


#         total_expenses = home_loan_emi + car_loan_emi + expenses



#         if (home_loan_emi + car_loan_emi) > 0.3 * income:
#             home_loan_warning = "Warning: Home loan and car loan EMI exceed 30% of income."

#         if total_expenses > 0.7 * income:
#             expenses_warning = "Warning: Total expenses exceed 70% of income."

#         # Calculate other results if needed...

#     return render(request, 'finance_calculator.html', {'result': result, 'home_loan_warning': home_loan_warning, 'expenses_warning': expenses_warning})









from math import pow


def retirement_planner(request):
    result = None

    if request.method == 'POST':
        income = float(request.POST.get('income'))
        retirement_income_goal = float(request.POST.get('retirement_income_goal'))
        years_until_retirement = int(request.POST.get('years_until_retirement'))

        # Calculate monthly investment needed for retirement
        annual_rate = 0.1  # 10% annual return
        monthly_rate = (1 + annual_rate) ** (1 / 12) - 1  # Monthly rate based on annual rate
        months = years_until_retirement * 12  # Convert years to months

        # Formula for monthly investment using compound interest formula
        monthly_investment = (retirement_income_goal * monthly_rate) / ((1 + monthly_rate) ** months - 1)

        result = f"To reach a retirement income goal of ${retirement_income_goal} in {years_until_retirement} years at 10% annual compounding returns, you need to invest approximately ${round(monthly_investment, 2)} monthly."

    return render(request, 'retirement_planner.html', {'result': result})





def emergency_fund_calculator(request):
    result = None

    if request.method == 'POST':
        income_needed = request.POST.get('income_needed')

        if income_needed:
            income_needed = float(income_needed)
            fund_six_months = income_needed * 6
            fund_twelve_months = income_needed * 12

            result = f"To cover 6 months of expenses, save approximately ${fund_six_months}. To cover 12 months, save approximately ${fund_twelve_months}."

    return render(request, 'emergency_fund_calculator.html', {'result': result})














from math import pow

def compound_interest_calculator(request):
    result = None
    annually = None

    if request.method == 'POST':
        monthly_income = float(request.POST.get('monthly_investment', 0))
        interest_rate = float(request.POST.get('interest_rate', 0)) / 100  # Convert percentage to decimal
        time_years = float(request.POST.get('time_years', 0))
        principal_amount = float(request.POST.get('principal_amount', 0))


        compound_amount = principal_amount * pow((1 + interest_rate), time_years)

        annually = round(compound_amount, 2)

        months = time_years * 12  # Total months
        monthly_rate = 1 + interest_rate / 12  

        compound = 0
        for month in range(int(months)):
            compound += monthly_income
            compound *= monthly_rate

        result = round(compound, 2)

    return render(request, 'compound_interest_calculator.html', {'result': result , 'annually' : annually})


def business_calculator(request):
    result = None
    warning_messages = []

    if request.method == 'POST':
        # startup_costs = float(request.POST.get('startup_costs', 0))
        rent = float(request.POST.get('rent', 0))
        salaries = float(request.POST.get('salaries', 0))
        insurance = float(request.POST.get('insurance', 0))
        # financing_options = float(request.POST.get('financing_options', 0))
        marketing_budget = float(request.POST.get('marketing_budget', 0))
        tax_amount = float(request.POST.get('tax_planning', 0))
        legal_and_compliance_costs = float(request.POST.get('legal_and_compliance_costs', 0))
        emergency_funds = float(request.POST.get('emergency_funds', 0))
        # owner_spending = float(request.POST.get('owner_spending', 0))

        total_expenses = (
            rent + salaries + insurance +
             marketing_budget + tax_amount +
            legal_and_compliance_costs + emergency_funds
        )

        # Check if expenses exceed certain percentages
        if rent > 0.05 * (rent + salaries + insurance):
            warning_messages.append("It's not recommended to invest more than 5% in rent.")

        if salaries > 0.15 * (rent + salaries + insurance):
            warning_messages.append("It's not recommended to invest more than 15% in salaries.")

        if insurance > 0.10 * (rent + salaries + insurance):
            warning_messages.append("It's not recommended to invest more than 10% in insurance.")

        if legal_and_compliance_costs > 0.05 * (rent + salaries + insurance):
            warning_messages.append("It's not recommended to invest more than 5% in legal and compliance costs.")

        if tax_amount > 0.20 * (rent + salaries + insurance):
            warning_messages.append("It's not recommended to invest more than 20% in tax planning.")

        # Calculate emergency fund
        emergency_fund_for_rent_salaries_insurance = 4 * (rent + salaries + insurance)

        result = {
            'total_expenses': total_expenses,
            'warning_messages': warning_messages,
            'emergency_fund_for_rent_salaries_insurance': emergency_fund_for_rent_salaries_insurance,
        }

        # if owner_spending > 0.20 * total_expenses:
        #     warning_messages.append("It's not recommended for the owner to spend more than 20% of total expenses.")
        #     result['warning_messages'] = warning_messages

    return render(request, 'business_calculator.html', {'result': result})













def calculate_loan(request):
    if request.method == 'POST':
        income = float(request.POST['income'])
        interest_rate = float(request.POST['interest_rate'])
        total_amount = float(request.POST['total_amount'])
        emi = float(request.POST['emi'])
        total_years = int(request.POST['total_years'])

        # Calculate total EMI
        total_emi = emi * 12 * total_years

        # Calculate the amount to pay every 3 months to reduce the loan
        quarterly_payment = 0.3 * income 

        # Calculate how many years reduced to pay the loan
        # reduced_years = (total_amount - quarterly_payment) / (emi * 12)

        remaining_amount = total_amount
        reduced = 0

        # Calculate how many years reduced to pay the loan
        while remaining_amount > 0:
            # Calculate interest for the current remaining amount
            interest_payment = (interest_rate / 100) * remaining_amount / 12

            # Calculate payment towards the principal amount
            quarterly_payment = 0.3 * income
            principal_payment = emi * 3 - interest_payment * 3  # Payment towards principal every 3 months

            amount_remain = principal_payment + quarterly_payment


            # Update remaining amount after payment
            remaining_amount -= amount_remain

            # Update reduced years
            reduced += 0.25  # 0.25 years for every 3 months

            reduced_years = total_years - reduced

        # return reduced_years

        # Calculate money saved
        money_saved = total_emi - (quarterly_payment * (total_years * 4))

        return render(request, 'calculate_loan.html', {
            'total_emi': total_emi,
            'reduced_years': reduced_years,
            'money_saved': money_saved,
        })

    return render(request, 'calculate_loan.html')

















































from django.shortcuts import render

def mortgage_calculator(request):
    if request.method == 'POST':
        home_price = float(request.POST.get('home_price'))
        down_payment_percent = float(request.POST.get('down_payment_percent'))
        loan_term_years = int(request.POST.get('loan_term_years'))
        interest_rate = float(request.POST.get('interest_rate'))
        property_tax_percent = float(request.POST.get('property_tax_percent'))
        home_insurance = float(request.POST.get('home_insurance'))
        other_costs = float(request.POST.get('other_costs'))

        # Calculate down payment amount
        down_payment = (down_payment_percent / 100) * home_price

        # Calculate loan amount
        loan_amount = home_price - down_payment

        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12

        # Calculate number of monthly payments
        num_payments = loan_term_years * 12

        # Calculate monthly mortgage payment
        if monthly_interest_rate != 0:
            mortgage_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
        else:
            mortgage_payment = loan_amount / num_payments

        # Calculate property tax amount
        property_tax = (property_tax_percent / 100) * home_price / 12

        # Calculate total monthly cost
        total_monthly_cost = mortgage_payment + property_tax + home_insurance + other_costs

        return render(request, 'mortgage_calculator.html', {
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'mortgage_payment': mortgage_payment,
            'property_tax': property_tax,
            'total_monthly_cost': total_monthly_cost,
            'home_price': home_price,
            'down_payment_percent': down_payment_percent,
            'loan_term_years': loan_term_years,
            'interest_rate': interest_rate,
            'property_tax_percent': property_tax_percent,
            'home_insurance': home_insurance,
            'other_costs': other_costs,
        })
    
    return render(request, 'mortgage_calculator.html')



















































####### new features 
######
#####
####
###
##
#





from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from moviepy.editor import VideoFileClip
import os

def extract_audio(request):
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)

        # Get the uploaded video file path
        uploaded_file_path = fs.url(filename)

        # Extract audio from the uploaded video using MoviePy
        # video_clip = VideoFileClip(settings.MEDIA_ROOT + uploaded_file_path[len('media/'):])

        # video_clip = VideoFileClip(settings.MEDIA_ROOT + uploaded_file_path)
        video_clip = VideoFileClip(os.path.join(settings.MEDIA_ROOT, filename))

        audio_clip = video_clip.audio

        # Define the directory to save the audio file
        extracted_audio_dir = os.path.join(settings.MEDIA_ROOT, 'extracted_audio')

        # Create the directory if it doesn't exist
        if not os.path.exists(extracted_audio_dir):
            os.makedirs(extracted_audio_dir)

        # Define the audio file path inside the 'extracted_audio' directory
        audio_filename = f"audio_{filename.split('.')[0]}.mp3"
        audio_path = os.path.join(extracted_audio_dir, audio_filename)

        # Save the extracted audio file to the specified path
        audio_clip.write_audiofile(audio_path)

        return render(request, 'audio_extraction.html', {'audio_filename': audio_path})

    return render(request, 'audio_extraction.html')

# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from moviepy.editor import VideoFileClip

# def extract_audio(request):
#     if request.method == 'POST' and request.FILES['video']:
#         video_file = request.FILES['video']
#         fs = FileSystemStorage()
#         filename = fs.save(video_file.name, video_file)

#         # Get the uploaded video file path
#         uploaded_file_path = fs.url(filename)

#         # Extract audio from the uploaded video using MoviePy
#         # video_clip = VideoFileClip(settings.MEDIA_ROOT + uploaded_file_path)
#         # video_clip = VideoFileClip(uploaded_file_path)
#         video_clip = VideoFileClip(settings.MEDIA_ROOT + uploaded_file_path[len('media/'):])

#         audio_clip = video_clip.audio
#         audio_filename = f"audio_{filename.split('.')[0]}.mp3"
#         audio_clip.write_audiofile(settings.MEDIA_ROOT + audio_filename)

#         return render(request, 'audio_extraction.html', {'audio_filename': audio_filename})

#     return render(request, 'audio_extraction.html')










from django.shortcuts import render
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def mix_youtube_videos(request):
    if request.method == 'POST':
        video_links = request.POST.get('video_links')
        video_links = video_links.split(',')[:10]  # Split by comma and limit to 10 links

        video_clips = []
        for link in video_links:
            try:
                yt = YouTube(link.strip())  # Remove leading/trailing whitespaces
                video = yt.streams.filter(file_extension='mp4').first()
                video.download('media/mix')  # Download the video

                # Load the downloaded video and extract a 2-3 minute clip
                video_path = f"media/mix/{video.default_filename}"
                video_clip = VideoFileClip(video_path).subclip(60, 120)  # Extracts 2-3 mins
                video_clips.append(video_clip)
            except Exception as e:
                print(f"Error processing {link}: {e}")  # Handle any errors in processing links

        # Concatenate all the 2-3 minute clips
        final_clip = concatenate_videoclips(video_clips)

        # Write the mixed video file
        final_clip.write_videofile('media/mix/mixed_video.mp4', codec='libx264')

        # Remove individual video clips after merging
        for link in video_links:
            try:
                yt = YouTube(link.strip())
                video = yt.streams.filter(file_extension='mp4').first()
                video_path = f"media/mix/{video.default_filename}"
                os.remove(video_path)
            except Exception as e:
                print(f"Error removing {link} video clip: {e}")  # Handle any errors in removing video clips
         
        # os.remove(video) 
        # os.remove(video_clip) 

        return render(request, 'mixmusic.html')

    return render(request, 'mixmusic.html')






























# import speech_recognition as sr
# from django.shortcuts import render
# from django.http import HttpResponse

# def transcribe_audio(request):
#     if request.method == 'POST' and request.FILES['audio_file']:
#         audio_data = request.FILES['audio_file']
#         recognizer = sr.Recognizer()
        
#         try:
#             with sr.AudioFile(audio_data) as source:
#                 audio_text = recognizer.recognize_google(source)
#                 # You can use different APIs for transcription, adjust parameters, etc.
                
#             return render(request, 'audio_to_text.html', {'audio_text': audio_text})
        
#         except sr.UnknownValueError:
#             error_message = "Could not understand the audio"
#             return render(request, 'audio_to_text.html', {'error_message': error_message})
    
#     return render(request, 'audio_to_text.html')


import speech_recognition as sr
# from pydub import AudioSegment
from django.shortcuts import render
from django.http import HttpResponse

def convert_to_supported_format(audio_file):
    # Load the audio file using pydub
    AudioSegment = 10
    sound = AudioSegment.from_file(audio_file)

    # Convert the audio to WAV format (you can change the format if needed)
    audio_wav = sound.export(format="wav")

    return audio_wav

def transcribe_audio(request):
    if request.method == 'POST' and request.FILES['audio_file']:
        audio_data = request.FILES['audio_file']
        
        # Convert the audio file to a supported format
        converted_audio = convert_to_supported_format(audio_data)
        
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(converted_audio) as source:
                audio_text = recognizer.recognize_google(source)
                # You can use different APIs for transcription, adjust parameters, etc.
                
            return render(request, 'audio_to_text.html', {'audio_text': audio_text})
        
        except sr.UnknownValueError:
            error_message = "Could not understand the audio"
            return render(request, 'audio_to_text.html', {'error_message': error_message})
    
    return render(request, 'audio_to_text.html')













# from django.shortcuts import render
# from gtts import gTTS
# import tempfile
# import os
from django.shortcuts import render
from gtts import gTTS
import os

def text_to_speech(request):
    audio_src = None
    
    if request.method == 'POST':
        text = request.POST.get('text')

        # Check if text is provided
        if text:
            # Create a gTTS object
            tts = gTTS(text)

            # Create directory if it doesn't exist
            audio_folder = 'media/audio/'
            os.makedirs(audio_folder, exist_ok=True)

            # Define file path for the audio
            file_path = os.path.join(audio_folder, 'output.mp3')

            # Save the audio to the specified file path
            tts.save(file_path)

            # Get the URL of the saved audio
            # audio_src = '/' + file_path.replace('media/', '')
            audio_src = os.path.join(settings.MEDIA_URL, 'audio', 'output.mp3')

    # If no text or if method is not POST, render the form
    return render(request, 'text_to_audio.html', {'audio_src': audio_src})



















from django.core.files.base import ContentFile
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def enhance_image(image):
    # Convert Django ImageField to OpenCV format
    img_cv2 = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Saturation adjustment
    img_hsv = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)
    # Modify the saturation channel, e.g., increase by 50%
    img_hsv[:, :, 1] = np.clip(img_hsv[:, :, 1] * 1.5, 0, 255)
    img_saturation = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    # Color balance adjustment
    img_color_balanced = img_cv2.copy()
    img_color_balanced[:, :, 0] = np.clip(img_color_balanced[:, :, 0] * 1.2, 0, 255)

    # Sharpness enhancement
    img_sharp = cv2.GaussianBlur(img_cv2, (0, 0), 3)
    img_sharp = cv2.addWeighted(img_cv2, 1.5, img_sharp, -0.5, 0)

    # Noise reduction using fastNlMeansDenoising
    img_denoised = cv2.fastNlMeansDenoisingColored(img_cv2, None, 10, 10, 7, 15)

    # Clarity enhancement (using unsharp masking)
    img_clarity = cv2.addWeighted(img_cv2, 1.5, cv2.GaussianBlur(img_cv2, (0, 0), 10), -0.5, 0)

    # Resizing (increase pixels while keeping size same)
    # Example: Upscale by 2x using cubic interpolation
    img_resized = cv2.resize(img_cv2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

      # White balance adjustment - Modify color channels accordingly
    # Example: Increase blue channel intensity for a cooler tone
    img_white_balance = img_cv2.copy()
    img_white_balance[:, :, 0] = np.clip(img_white_balance[:, :, 0] * 1.2, 0, 255)

    # Vibrance adjustment - Increase intensity of less saturated colors
    # Example: Increase vibrance by boosting less saturated colors in HSV space
    img_vibrance = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)
    vibrance_factor = 1.5
    img_vibrance[:, :, 1] = np.clip(img_vibrance[:, :, 1] * vibrance_factor, 0, 255)
    img_vibrance = cv2.cvtColor(img_vibrance, cv2.COLOR_HSV2BGR)

    # Hue/Saturation adjustments - Manipulate hue and saturation levels
    # Example: Increase overall saturation and shift hue
    img_hsv_adjusted = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV)
    img_hsv_adjusted[:, :, 1] = np.clip(img_hsv_adjusted[:, :, 1] * 1.2, 0, 255)
    img_hsv_adjusted[:, :, 0] = (img_hsv_adjusted[:, :, 0] + 20) % 180  # Shift hue by 20 degrees
    img_hue_saturation_adjusted = cv2.cvtColor(img_hsv_adjusted, cv2.COLOR_HSV2BGR)

    # Levels & Curves adjustments - Modify brightness, contrast, gamma correction
    # Example: Adjust brightness and contrast
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 50    # Brightness control (0-100)
    img_levels_curves = cv2.convertScaleAbs(img_cv2, alpha=alpha, beta=beta)

    # Convert back to Django ImageField format
    img_pil = Image.fromarray(cv2.cvtColor(img_saturation, cv2.COLOR_BGR2RGB))
    buffer = BytesIO()
    img_pil.save(buffer, format='JPEG')
    img_content = ContentFile(buffer.getvalue())
    return img_content








# def upload_and_enhance(request):
#     form =  ImageUploadForm(request.POST or None, request.FILES or None)
    
#     if request.method == 'POST' and form.is_valid():
#         uploaded_image = form.save()  # Save the form data to the UploadedImage model

#         # Assume `enhance_image()` is a function that enhances the image
#         enhanced_image = enhance_image(uploaded_image.original_image)  

#         # Update the UploadedImage instance with the enhanced image and save
#         uploaded_image.enhanced_image.save(uploaded_image.original_image.name, enhanced_image)
#         uploaded_image.save()

#         return render(request, 'image_enhance.html', {'uploaded_image': uploaded_image , 'enhanced_image' :enhanced_image})

#     return render(request, 'image_enhance.html', {'form': form})

from django.core.files.base import ContentFile

def upload_and_enhance(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        uploaded_image = form.save()  # Save the form data to the UploadedImage model

        # Assume `enhance_image()` is a function that enhances the image
        enhanced_image = enhance_image(uploaded_image.original_image)

        # If `enhance_image()` returns a file-like object, save it using ContentFile
        enhanced_image_io = ContentFile(enhanced_image.read())
        uploaded_image.enhanced_image.save(uploaded_image.original_image.name, enhanced_image_io)
        uploaded_image.save()

        return render(request, 'image_enhance.html', {'uploaded_image': uploaded_image})

    return render(request, 'image_enhance.html', {'form': form})

# def upload_and_enhance(request):
#     form = ImageUploadForm(request.POST or None, request.FILES or None)

#     if request.method == 'POST' and form.is_valid():
#         uploaded_image = form.save(commit=False)  # Create UploadedImage instance without saving to DB
#         uploaded_image.save()  # Save the original image to the DB

#         enhanced_image = enhance_image(uploaded_image.original_image)  # Process the image
#         uploaded_image.enhanced_image.save(uploaded_image.original_image.name, enhanced_image)  # Save enhanced image

#         return render(request, 'img_enhance.html.html', {'uploaded_image': uploaded_image})

#     return render(request, 'img_enhance.html', {'form': form})


























# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





















































####### Ai website 
######
#####
####
###
##
#

def aiwebsite(request):
    return render (request , 'web_AI_home.html' )
























































####### blog creation purpose
######
#####
####
###
##

class BlogListView(ListView):
     model = Blog
     template_name = 'blog_creation.html'
     context_object_name = 'blogs'
     ordering = ['-dateposted']



class BlogDetailView(DetailView):
     model = Blog
     template_name = 'blog_detail.html'

     
class BlogCreateView(LoginRequiredMixin , imguploadform,CreateView):
    model = Blog
    template_name = 'blog_upload.html'



    def form_valid (self ,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   


        

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin,imguploadform ,UpdateView):
    model = Blog
    template_name = 'postform.html'

    def form_valid (self ,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True      
        return False
   


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
     model = Blog
     template_name = 'blogdelete.html'
     success_url = reverse_lazy('blog')

     def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False





















































####### courses
######
#####
####
###
##
#


# views.py
from django.shortcuts import render

def skill_improvement(request):
    query = request.GET.get('query')
    links = []

    if query:
        # Create a list of 10 specific links with the user's input
        links = [
            f"https://www.khanacademy.org/search?referer=%2Fmath%2Falgebra&page_search_query={query}",
            f"https://www.freecodecamp.org/news/search?query={query}",
            f"https://www.codecademy.com/search?query={query}",
            f"https://www.futurelearn.com/search?q={query}",

            f"https://online.stanford.edu/explore?keywords={query}&items_per_page=12&filter%5B0%5D=free_or_paid%3Afree",
            f"https://pll.harvard.edu/catalog?keywords={query}",

            f"https://www.edx.org/search?q={query}",
            f"https://oli.cmu.edu/?s={query}",
            f"https://www.sololearn.com/learn",

            f"https://alison.com/courses?query={query}",
            f"https://ed.ted.com/search?qs={query}",
            f'https://grow.google/grow-your-business/#?modal_active=none',
            f'https://grow.google/grow-your-career/#?modal_active=none',
        ]

    return render(request, 'skillimprove.html', {'query': query, 'links': links})



# https://openlearning.mit.edu/courses-programs/mitx-courses?f%5B0%5D=course_availability%3A62&f%5B1%5D=course_availability%3A63&f%5B2%5D=course_availability%3A64&f%5B3%5D=course_availability%3A128&f%5B4%5D=course_availability%3A129&f%5B5%5D=course_department%3A7&f%5B6%5D=course_department%3A16&f%5B7%5D=course_department%3A22&f%5B8%5D=course_department%3A23&f%5B9%5D=course_department%3A24&f%5B10%5D=course_department%3A25&f%5B11%5D=course_department%3A26&f%5B12%5D=course_department%3A32&f%5B13%5D=course_department%3A34&f%5B14%5D=course_department%3A38&f%5B15%5D=online_learning_platform%3Aedx_course&f%5B16%5D=online_learning_platform%3Amitx_course&search_api_fulltext=biology%20course


# https://grow.google/grow-your-career/#?modal_active=none
# https://grow.google/grow-your-business/#?modal_active=none



# https://www.khanacademy.org/search?referer=%2Fmath%2Falgebra&page_search_query=computer+course
# https://ed.ted.com/search?qs=train+brain+to+get+better
# https://www.edx.org/search?q=computer+graphics
# https://pll.harvard.edu/catalog?keywords=finance+course ###
# https://online.stanford.edu/explore?keywords=information%20technology&items_per_page=12&filter%5B0%5D=free_or_paid%3Afree
# https://oli.cmu.edu/?s=engineering+course ###
# https://www.codecademy.com/search?query=ai
# https://www.sololearn.com/learn
# https://www.freecodecamp.org/news/search?query=engineering
# https://alison.com/courses?query=micro%20biology
# https://www.futurelearn.com/search?q=business%20strategy































































#######  Seo Purpose AI Features
######
#####
####
###
##
#






def SEO_defination(request):
    return render(request , 'blog_post1.html')

def Content(request):
    return render(request , 'blog_post2.html')

def aiuses(request):
    return render(request , 'blog_post3.html')

def wordpress(request):
    return render (request , 'blog_post4.html')

def googleadsense(request):
    return render (request , 'blog_post5.html')

def chatgpt(request):
    return render (request , 'blog_post6.html')

def features(request):
    return render (request , 'all_features.html')



def daily_scope(request):
    return render (request , 'daily_scope.html')

def keyword_volume_difficulty(request):
    return render (request, 'keyword_volume_difficulty.html')

def broken_competitor(request):
    return render (request , 'broken_competitor.html')

def technical_onpage (request):
    return render (request , 'technical_onpage.html')













def check_readability(url):
    if len(url) > 50:  
        return 'URL is not readable'

    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    if any(char in url for char in special_characters):
        return 'URL contains special characters remove the characters'

    return 'URL is readable'


# @login_required
# @premium_user_required
def find_broken_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        secure_links = []
        broken_links = []


        def is_link_secure(link_url):
            parsed_url = urlparse(link_url)
            return parsed_url.scheme == 'https' or parsed_url.scheme == 'shttps'

       
        links_with_target = defaultdict(int)

        for link in links:
            link_url = link.get('href')

            if link_url.startswith('http'):
                if is_link_secure(link_url):
                    secure_links.append(link_url)
                    Link.objects.create(url=link_url, is_secure=True)
                else:
                    broken_links.append(link_url)
                    Link.objects.create(url=link_url, is_secure=False)

                link_target = link.get('target')
                if link_target is not None:
                    links_with_target[link_url] += 1

        total_links = len(secure_links) + len(broken_links)

##
        url_structure = check_readability(url)
###
        return render(request, 'broken_link_result.html', {
            'total_links': total_links,
            'secure_links': secure_links,
            'broken_links': broken_links,
            'links_with_target': links_with_target,
            'url_structure': url_structure,
        })
    return render(request, 'broken_link_result.html')












def check_website_security(url):
    is_https = url.startswith('https://')

    has_valid_certificate = False
    if is_https:
        try:
            response = requests.get(url)
            has_valid_certificate = response.ok
        except requests.exceptions.SSLError:
            pass

    def has_secure_password_policy(soup):
        
        min_password_length = 8 
        password_field = soup.find('input', {'type': 'password'})
        if password_field:
            if len(password_field.get('pattern', '')) > 0:
                pattern = password_field['pattern']
                pattern_match = re.search(r'\{\d+\}', pattern)
                if pattern_match:
                    min_password_length = int(pattern_match.group()[1:-1])

        if min_password_length >= 12:
            if re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)', pattern):
                return True

        return False

    def has_secure_authentication(soup):
       
        uses_2fa = False  

        two_factor_auth_elements = soup.find_all('input', {'type': 'text', 'autocomplete': 'one-time-code'})
        if two_factor_auth_elements:
            uses_2fa = True

        return uses_2fa


    def follows_secure_development_practices(soup):
         
         follows_practices = False 

         inputs = soup.find_all('input')
         for input_field in inputs:
             if input_field.get('type') == 'text':
                 if input_field.get('oninput') or input_field.get('onblur'):
                     follows_practices = True
                     break

             if input_field.get('type') == 'textarea':
                 if input_field.get('oninput') or input_field.get('onblur'):
                     follows_practices = True
                     break

         return follows_practices

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    has_secure_password_policy_result = has_secure_password_policy(soup)
    has_secure_authentication_result = has_secure_authentication(soup)
    follows_secure_development_practices_result = follows_secure_development_practices(soup)


    return {
        'is_https': is_https,
        'has_valid_certificate': has_valid_certificate,
        'has_secure_password_policy': has_secure_password_policy_result,
        'has_secure_authentication': has_secure_authentication_result,
        'follows_secure_development_practices': follows_secure_development_practices_result,
    }


# @login_required
# @premium_user_required
def technical_seo_analysis(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        response = requests.get(url)
        site_speed = response.elapsed.total_seconds()
        
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        mobile_response = requests.get(url, headers=headers)
        mobile_friendly = 'Yes' if mobile_response.status_code == 200 else 'No'
        
        protocol = 'HTTPS' if url.startswith('https://') else 'HTTP'
        
        custom_error = None
        if response.status_code >= 400:
            custom_error = response.status_code
        security_results = check_website_security(url)
        
        
        context = {
            'url': url,
            'site_speed': site_speed,
            'mobile_friendly': mobile_friendly,
            'protocol': protocol,
            'security_results': security_results,
            'custom_error': custom_error,
        }
        
        return render(request, 'technical_seo_result.html', context)
    
    return render(request, 'technical_seo_result.html')















# @login_required
# @premium_user_required
def crawl_website_properly(request):

    if request.method == 'POST':
        url = request.POST.get('url')  
       
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        page_title = soup.title.text if soup.title else None

        urls = [link['href'] for link in soup.find_all('a', href=True)]

        meta_tags = soup.find_all('meta')
        metadata = {}
        for tag in meta_tags:
            if tag.get('name'):
                metadata[tag.get('name')] = tag.get('content')

        headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

        text_content = soup.get_text()

        images = []
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_src = img.get('src')
            alt_text = img.get('alt')
            images.append({'src': img_src, 'alt': alt_text})

        structured_data = soup.find_all('script', type='application/ld+json')

        return render(request, 'crawl_result.html', {
            'page_title': page_title,
            'urls': urls,
            'metadata': metadata,
            'headings': headings,
            'text_content': text_content,
            'images': images,
            'structured_data': structured_data
        })

    return render(request, 'crawl_result.html')










# @login_required
# @premium_user_required

def real_time_trend(request):
    if request.method == 'POST':
        country = request.POST.get('country')

        # Google daily search trends
        today_trends = daily_trends(country=country)

        context = {
            'country': country,
            'real_time_trends': today_trends,
        }
        return render(request, 'trending_google.html', context)

    return render(request, 'trending_google.html')

# def real_time_trend(request):
#     if request.method == 'POST':
#         country = request.POST.get('country')
#         # country = 'country'

#         pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 10))
#         pytrends.build_payload(kw_list=['default'], cat=0, timeframe='now 1-d', geo=country)

#         # pytrends.build_payload(kw_list=['default'],  cat=0, timeframe='now 1-d',geo=country)
# # cat=0,
#         real_time_trends_df = pytrends.trending_searches(pn=country)

#         # real_time_trends_df = pytrends.trending_searches(pn='germany')
#         real_time_trends = real_time_trends_df[0].tolist()


#         context = {
#             'country': country,
#             'real_time_trends': real_time_trends,
#         }
#         return render(request, 'trending_google.html', context)

#     return render(request, 'trending_google.html')














# @login_required
# @premium_user_required

def keyword_difficulty(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        country = request.POST.get('country')
# , lang='en'
        websites = list(search(keyword, country=country))[:10]

        results = []
        count_present = 0  

        for website in websites:
            result = {'url': website, 'meta_count': 0, 'heading_count': 0}

            try:
                response = requests.get(website)
                soup = BeautifulSoup(response.text, 'html.parser')

                meta_tags = soup.find_all('meta', {'content': keyword})
                result['meta_count'] = len(meta_tags)

                heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                for tag in heading_tags:
                    if keyword in tag.get_text():
                        result['heading_count'] += 1

                if result['meta_count'] > 0 or result['heading_count'] > 0:
                    count_present += 1

            except requests.exceptions.RequestException:
                pass

            results.append(result)

            time.sleep(1)

        sorted_results = sorted(results, key=lambda x: x['meta_count'] + x['heading_count'], reverse=True)

        multiplied_count = count_present * 10
####
        search_results = []
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                search_results = list(search(keyword ,country=country))
                break
            except Exception as e:
                retries += 1
                time.sleep(1)  
####
        return render(request, 'keyword_difficulty.html', {'results': search_results ,'keyword': keyword, 'results': sorted_results,  'multiplied_count': multiplied_count})
    
    return render(request, 'keyword_difficulty.html')



# def testing(request):
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword')
#         country = request.POST.get('country')

#         search_results = []
#         max_retries = 3
#         retries = 0

#         while retries < max_retries:
#             try:
#                 search_results = list(search(keyword ,country=country))
#                 break
#             except Exception as e:
#                 retries += 1
#                 time.sleep(1)  

#         context = {'results': search_results}
#         return render(request, 'keyword_difficulty.html', context)

#     return render(request, 'keyword_difficulty.html')












# @login_required
# @premium_user_required
def keyword_scope(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
        country = request.POST.get('country')

        # Create a datetime object from the given year and month
        start_date = datetime.datetime(year, month, 1).date()
        end_date = start_date + datetime.timedelta(days=30)

        # Set up the pytrends object
        pytrend = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1, timeout=10)

        # Set the search keyword and the time range
        pytrend.build_payload(kw_list=[keyword], timeframe=f'{start_date} {end_date}', geo=country)

        # Retrieve the data
        related_queries = pytrend.related_queries()
        related_queries_values = related_queries.values()

        related_topic = pytrend.related_topics()
        related_topic_values = related_topic.values()

##
        url = f"https://trends.google.com/trends/explore?q={keyword}&date={start_date.strftime('%Y-%m')}"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        related_websites_values = []
        website_elements = soup.select('.related-entities .details-text a')
        for website_element in website_elements:
            title = website_element.text
            link = website_element['href']
            website = {'title': title, 'link': link}
            related_websites_values.append(website)

        return render(request, 'google_trend.html', {
            'keyword': keyword,
            'related_queries': related_queries_values,
            'related_topic': related_topic_values,
            'related_websites': related_websites_values,


        })

    return render(request, 'google_trend.html')

















# import google_trends



# def Keyword_volume(request):
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword')
#         country = request.POST.get('country')
#         time_range = request.POST.get('time_range')
#         category = request.POST.get('category')

#         # volume_data = google_trends.get_trends(keyword, hl='en-US', geo=country, timeframe=time_range, cat=category)

#         # search_topic = request.POST.get('search_topic')

#         pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 10))
        
#         # if search_topic == 'web_search':
#         pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=time_range, geo=country, gprop='')
#         trends_data = pytrends.interest_over_time()
#         # elif search_topic == 'image_search':
#         #     pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=time_range, geo=country, gprop='images')
#         #     trends_data = pytrends.trending_searches(pn=country)
#         # elif search_topic == 'youtube_search':
#         #     pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=time_range, geo=country, gprop='youtube')
#         #     trends_data = pytrends.top_charts(category='Video', date=time_range, geo=country)

#         time.sleep(3)

#         context = {
#             'keyword': keyword,
#             'country': country,
#             'time_range': time_range,
#             'category': category,
#             # 'volume' : volume_data,
#             # 'search_topic': search_topic,
#             'trends_data': trends_data,
#             'search_count': range(len(trends_data)+1),  # Add this line

#         }
#         return render(request, 'google_search_volume.html', context)

#     return render(request, 'google_search_volume.html')



# @login_required
# @premium_user_required

def Keyword_volume(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        country = request.POST.get('country')
        time_range = request.POST.get('time_range')
        category = request.POST.get('category')

        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 10))
        pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=time_range, geo=country, gprop='')
        trends_data = pytrends.interest_over_time()

        time.sleep(3)

        context = {
            'keyword': keyword,
            'country': country,
            'time_range': time_range,
            'category': category,
            'trends_data': trends_data,
            'search_count': range(len(trends_data) + 1),
        }
        return render(request, 'google_search_volume.html', context)

    return render(request, 'google_search_volume.html')











# @login_required
# @premium_user_required


def Onpage_seo(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        file = request.FILES.get('file')

        if url:
            response = requests.get(url)
            html_content = response.text
        elif file:
            html_content = file.read().decode('utf-8')
        else:
            return render(request, 'html_structure_result.html')

        soup = BeautifulSoup(html_content, 'html.parser')
        header = soup.find('header')
        main = soup.find('main')
        footer = soup.find('footer')

        missing_tags = []

        if header is None:
            missing_tags.append('header')
        if main is None:
            missing_tags.append('main')
        if footer is None:
            missing_tags.append('footer')

        img_count = 0

        if header:
            nav = header.find('nav')
            if nav is None:
                missing_tags.append('nav')
            else:
                if not nav.find('li') and not nav.find('ul'):
                    missing_tags.append('li or ul')

        images = soup.find_all('img')
        for image in images:
            alt_text = image.get('alt')
            if not alt_text or len(alt_text.split()) < 5:
                img_count += 1

        if header and main and footer:
            try:
                if soup.index(header) > soup.index(main) or soup.index(main) > soup.index(footer):
                    missing_tags.extend(['header', 'main', 'footer'])
            except ValueError:
                pass


            ##
        meta_keywords = []
        meta_tags = soup.find_all('meta', attrs={'name': 'description'})
        for meta in meta_tags:
            meta_keywords.extend(re.findall(r'\b\w+\b', meta.get('content', '').lower()))

        keyword_counts = Counter()

        specified_tags = ['meta', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
        for tag in specified_tags:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text().lower()
                keywords = re.findall(r'\b\w+\b', text)
                keyword_counts.update(keywords)

        excluded_words = ['a', 'an', 'the', '!', '.' , 'in' , 'is','you' ,'your']
        keyword_counts = {word: count for word, count in keyword_counts.items() if word not in excluded_words}

        weighted_keyword_counts = {}
        for word, count in keyword_counts.items():
            if word in meta_keywords:
                weighted_keyword_counts[word] = count * 10
            elif word.startswith('h'):
                weighted_keyword_counts[word] = count * 6
            else:
                weighted_keyword_counts[word] = count

        top_10_keywords = dict(sorted(weighted_keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10])


        # if missing_tags or img_count:
        #     return render(request, 'html_structure_result.html', {'missing_tags': missing_tags, 'img_count': img_count})
        # else:
        context ={'top_keywords': top_10_keywords ,'missing_tags': missing_tags, 'img_count': img_count} #, 'keyword_counts': weighted_keyword_counts
        return render(request, 'html_structure_result.html' , context)

    return render(request, 'html_structure_result.html')

