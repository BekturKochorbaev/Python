from django.urls import path
from .views import (
    UserAPIView, UserProfileListAPIView, HomeListAPIView, RegionListAPIView,
    AttractionsListAPIView, AttractionsDetailAPIView, AttractionReviewListAPIView,
    AttractionReviewDetailAPIView, AttractionReviewStaticListApiView,
    AttractionReviewCreateAPIView, ReplyToAttractionReviewView, PopularPlacesListAPI,
    PopularPlacesDetailAPI, PopularReviewListAPIView, PopularReviewDetailAPIView,
    PopularPlacesStaticAPIView, PopularReviewCreateAPIView, ReplyToPopularPlacesCreateView,
    HotelsListAPIView, HotelsDetailAPIView, HotelsReviewListAPIView,
    HotelsReviewDetailAPIView, HotelsReviewStaticListAPIView, HotelReviewCreateAPiView,
    ReplyToHotelReviewView, KitchenListView, KitchenDetailView, KitchenReviewCreateAPIView,
    KitchenReviewListAPIView, KitchenReviewDetailAPIView, KitchenReviewStaticAPIView,
    ReplyToKitchenReviewView, AirLineTicketsAPIView, EventListAPiView, TicketListAPIView,
    CultureListAPiView, GamesViewSet, CultureKitchenViewSet, CultureKitchenMainListViewSet,
    NationalClothesViewSet, CurrencyViewSet, HandCraftsViewSet, NationalInstrumentsViewSet,
    FavoriteCreateView, FavoriteDeleteView, FavoriteListView
)
from . import views
app_name = 'country'
urlpatterns = [
    path('xml/', views.upload_xml, name='xml'),

    path('user_profile_update/', UserAPIView.as_view(), name='user_profile_create'),
    path('user_profile_list/', UserProfileListAPIView.as_view(), name='user_profile_list'),

    path('home/', HomeListAPIView.as_view(), name='home'),
    path('region/', RegionListAPIView.as_view(), name='region'),

    path('attractions/', AttractionsListAPIView.as_view(), name='attractions'),
    path('attractions/<int:pk>/', AttractionsDetailAPIView.as_view(), name='attractions_detail'),
    path('attraction_review_list/', AttractionReviewListAPIView.as_view(), name='attraction_review_list'),
    path('attraction_review_list/<int:pk>/', AttractionReviewDetailAPIView.as_view(), name='attraction_review_detail'),
    path('attraction_review_static/', AttractionReviewStaticListApiView.as_view(), name='attraction_review_static'),
    path('attraction_review_create/', AttractionReviewCreateAPIView.as_view(), name='attraction_review_create'),
    path('reply_attraction_review/', ReplyToAttractionReviewView.as_view(), name='reply_attraction_review'),

    path('popular_places/', PopularPlacesListAPI.as_view(), name='region_popular_places'),
    path('popular_places/<int:pk>/', PopularPlacesDetailAPI.as_view(), name='region_popular_places_detail'),
    path('popular_places_review/', PopularReviewListAPIView.as_view(), name='popular_places_review'),
    path('popular_places_review/<int:pk>/', PopularReviewDetailAPIView.as_view(), name='popular_places_review'),
    path('popular_places_static/', PopularPlacesStaticAPIView.as_view(), name='popular_places_static'),
    path('popular_places_review_create/', PopularReviewCreateAPIView.as_view(), name='popular_places_review_create'),
    path('reply_popular_places/', ReplyToPopularPlacesCreateView.as_view(), name='reply_popular_places'),

    path('hotels/', HotelsListAPIView.as_view(), name='hotels_list'),
    path('hotels/<int:pk>/', HotelsDetailAPIView.as_view(), name='hotel_detail'),
    path('hotels_review_list/', HotelsReviewListAPIView.as_view(), name='hotels_review_list'),
    path('hotels_review_list/<int:pk>/', HotelsReviewDetailAPIView.as_view(), name='hotels_review_detail'),
    path('hotels_review_static/', HotelsReviewStaticListAPIView.as_view(), name='hotels_review_static'),
    path('hotels_review_create/', HotelReviewCreateAPiView.as_view(), name='hotels_review_create'),
    path('reply_hotel_reviews/', ReplyToHotelReviewView.as_view(), name='reply_hotel_reviews'),

    path('kitchen/', KitchenListView.as_view(), name='kitchen_list'),
    path('kitchen/<int:pk>/', KitchenDetailView.as_view(), name='kitchen_detail'),
    path('kitchen_review_create/', KitchenReviewCreateAPIView.as_view(), name='kitchen_review_create'),
    path('kitchen_review_list/', KitchenReviewListAPIView.as_view(), name='kitchen_review_list'),
    path('kitchen_review_list/<int:pk>/', KitchenReviewDetailAPIView.as_view(), name='kitchen_review_detail'),
    path('kitchen_review_static/', KitchenReviewStaticAPIView.as_view(), name='kitchen_review_static'),
    path('reply_kitchen_reviews/', ReplyToKitchenReviewView.as_view(), name='reply_kitchen_reviews'),

    path('airline_tickets/', AirLineTicketsAPIView.as_view(), name='airline_tickets'),

    path('event/', EventListAPiView.as_view(), name='event'),
    path('only_tickets/', TicketListAPIView.as_view(), name='only_tickets'),

    path('culture_list/', CultureListAPiView.as_view(), name='culture_list'),

    path('games/', GamesViewSet.as_view({'get': "list"}), name='games_list'),

    path('culture_kitchen/', CultureKitchenViewSet.as_view({'get': "list"}), name='culture_kitchen'),
    path('culture_kitchen_main/', CultureKitchenMainListViewSet.as_view({'get': "list"}), name='culture_kitchen_main'),

    path('national_clothes/', NationalClothesViewSet.as_view({'get': "list"}), name='national_clothes_list'),

    path('currency/', CurrencyViewSet.as_view({'get': "list"}), name='currency_list'),

    path('handcrafts/', HandCraftsViewSet.as_view({'get': "list"}), name='handcrafts_list'),

    path('instruments/', NationalInstrumentsViewSet.as_view({'get': "list"}), name='instruments_list'),


    path('favorites/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:favorite_id>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),


]
