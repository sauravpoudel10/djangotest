from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (BlogListView,
BlogDetailView,BlogCreateView,BlogUpdateView,
BlogDeleteView)
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name ='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name ='logout.html'), name='logout'),
    path('accounts/profile/<int:user_id>/', views.profile, name='profile'),


    path('skillimprovement/' , views.skill_improvement , name='skillimprovement'),
    path('Image-Enhancement/' , views.upload_and_enhance , name='image_enhancement'),###
    path('find_email/', views.email_find, name='email-find'), ###

    path('text_to_speech/' , views.text_to_speech , name='text_to_speech'),###
    path('audio_to_text/' , views.transcribe_audio , name='audio_to_text'),#
    path('create_music_mashup/' , views.mix_youtube_videos , name='mix_youtube_videos'), ###
    path('extract_audio_from_video/' , views.extract_audio , name='extract_audio'),#


    

    path('mortgage_calculator/' , views.mortgage_calculator, name='mortgage_calculator'),#

    path('calculate/', views.calculate_loan, name='calculate_loan'), ##
    path('calculate_growth-1/', views.calculate_growth, name='revenue1'),
    path('calculate_growth-2/', views.find_growth_business, name='revenue2'),
    path('business_calculator/', views.business_calculator, name='business_calculator'),##
    path('compound_interest_calculator/', views.compound_interest_calculator, name='compound_interest_calculator'), #add feature change over month year
    path('emergency_fund_calculator/', views.emergency_fund_calculator, name='emergency_fund_calculator'), ##
    path('retirement_planner/', views.retirement_planner, name='retirement_planner'),#ways to achieve 10%
    path('finance_calculator/', views.finance_calculator, name='finance_calculator'),






]


# Subdomain 'SEO Optimiser'
seo_patterns = [
    path('', TemplateView.as_view(template_name='seo.html'), name='seo'),
    path('broken-link-finder/', views.find_broken_link, name='broken_link'),
    path('technical-seo-analysis/', views.technical_seo_analysis, name='technical_seo'),
    path('competitor-web-analysis/', views.crawl_website_properly, name='crawl'),
    path('trending-topics/', views.real_time_trend, name='trending'),
    path('check-keyword-difficulty/', views.keyword_difficulty, name='keyword_difficulty'),
    path('keyword-scope/', views.keyword_scope, name='keyword_scope'),
    path('keyword-volume/', views.Keyword_volume, name='keyword_volume'),
    path('onpage-seo-analysis/', views.Onpage_seo, name='onpage_seo'),
    path('SEO-and-its-types-with-tips-to-rank-on-google/', views.SEO_defination, name='blog1'),
    path('Role-of-content-in-SEO-to-rank-top-on-google/', views.Content, name='blog2'),
    path('The-Use-of-AI-In-Content_Creation/', views.aiuses, name='blog3'),
    path('Build-working-Wordpress-website-From-Begining-In-2023/', views.wordpress, name='blog4'),
    path('Run-Ads-In-Your-website-Using-google-Adsense-In-2023/', views.googleadsense, name='blog5'),
    path('How-ChatGpt-Is-made-and-how-to-build-your-own-In-2023/', views.chatgpt, name='blog6'),
    path('all-features/', views.features, name='features'),
    path('How-to-find-keyword-Scope-Trend-for-SEO/', views.daily_scope, name='daily_scope'),
    path('Find-keyword-difficulty-and-Volume-for-Organic-Traffic/', views.keyword_volume_difficulty, name='volume-difficulty'),
    path('Analyse-Technical-And-Onpage-SEO-To-Rank-Top-On-Google/', views.technical_onpage, name='Onpage-technical'),
    path('Find-broken-link-and-analysis-competitor-postion-for-better-growth-of-website/', views.broken_competitor, name='broken_competitor'),
]


AI_website_patterns = [
    path('' , views.aiwebsite , name='aiweb'),
    path('select_&_download_website/', TemplateView.as_view(template_name='web-category-selection.html'), name='webcategoryselection'),



]



blog_patterns = [
path('' , BlogListView.as_view(), name ='blog'),
path('<int:pk>/' , BlogDetailView.as_view() , name='blogdetail'),
path('create/' , BlogCreateView.as_view() , name='blogcreate'),
path('<int:pk>/update/' , BlogUpdateView.as_view() , name='blogupdate'),
path('<int:pk>/delete/' , BlogDeleteView.as_view() , name='blogdelete'),

]


sclorship_patterns = [
path('' , views.scholarships_view, name='scholarship'),

]

aiwebsitefinder_patterns = [
path('' , views.search_ai_websites , name='findweb'),
]

ai_shortmaker_patterns = [
# path('workout/' , views.chat_view , name='workout'),
path('' , views.index, name='test'),
# path('download/<str:clip_name>/', views.download_clip, name='download_clip'),

]



urlpatterns += [
    # Include subdomain-specific patterns
    path('generate_website/' , include(AI_website_patterns)),
    path('SEO/', include(seo_patterns)),
    path('blog/' , include(blog_patterns)),
    path('Find-AI-Website/' , include(aiwebsitefinder_patterns)),

    path('Find-Scholarship/' , include(sclorship_patterns)),
    path('generate_short_clip/' , include(ai_shortmaker_patterns)),

    path('<path:invalid_path>', TemplateView.as_view(template_name='page_doesnot_exist.html'), name='does_not_exist'),

]

















