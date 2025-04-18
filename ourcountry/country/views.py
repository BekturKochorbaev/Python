from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework.response import Response
from django.db.models import Avg, Case, When, Value, IntegerField
from rest_framework import permissions
from rest_framework import filters
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserProfileSerializer, AttractionReviewListSerializer, AttractionReviewStaticSerializers,
    AttractionReviewCreateSerializer, ReplyToAttractionReviewSerializer, AttractionReviewSerializer,
    AttractionsListSerializer, AttractionsDetailSerializer, HomeSerializer, PopularPlacesListSerializer,
    PopularPlacesStaticSerializer, ReplyToPopularPlacesSerializer, ToTrySerializer, RegionSerializer,
    PopularReviewListSerializer, PopularReviewCreateSerializer, PopularPlacesDetailSerializer,
    HotelsListSerializer, HotelReviewListSerializer, HotelDetailSerializer, ReplyToHotelReviewSerializer,
    HotelsReviewCreateSerializer, HotelsReviewSerializer, HotelReviewStaticSerializers, KitchenListSerializer,
    KitchenReviewListSerializer, KitchenDetailSerializers, ReplyToKitchenReviewSerializer,
    KitchenReviewCreateSerializer, KitchenReviewStaticSerializers, EventSerializers, TicketsSerializers,
    CultureSerializers, CultureKitchenMainListSerializers, GamesSerializers, NationalClothesSerializers,
    HandCraftsSerializers, CurrencySerializers, NationalInstrumentsSerializers, CultureKitchenSerializers,
    PopularReviewSerializer, AirLineTicketsSerializers, FavoriteSerializer, FavoriteListSerializer,
    KitchenReviewSerializer
)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = UserProfile.objects.get(email=request.user.email)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(email=self.request.user.email)


class HomeListAPIView(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class AttractionsListAPIView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsListSerializer


class AttractionsDetailAPIView(generics.RetrieveAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsDetailSerializer


class AttractionReviewListAPIView(generics.ListAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = AttractionReviewFilter


class AttractionReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer


class AttractionReviewStaticListApiView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionReviewStaticSerializers


class AttractionReviewCreateAPIView(generics.CreateAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            attraction_review = serializer.save()
            response_serializer = AttractionReviewSerializer(attraction_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyToAttractionReviewView(generics.CreateAPIView):
    queryset = ReplyToAttractionReview.objects.all()
    serializer_class = ReplyToAttractionReviewSerializer


class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class PopularPlacesListAPI(generics.ListAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesListSerializer


class PopularPlacesDetailAPI(generics.RetrieveAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesDetailSerializer


class PopularReviewListAPIView(generics.ListAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = PopularReviewFilter


class PopularReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer


class PopularPlacesStaticAPIView(generics.ListAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesStaticSerializer


class PopularReviewCreateAPIView(generics.CreateAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            popular_review = serializer.save()
            response_serializer = PopularReviewSerializer(popular_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyToPopularPlacesCreateView(generics.CreateAPIView):
    queryset = ReplyToPopularReview.objects.all()
    serializer_class = ReplyToPopularPlacesSerializer


class ToTryViewSet(viewsets.ModelViewSet):
    queryset = ToTry.objects.all()
    serializer_class = ToTrySerializer


class HotelsListAPIView(generics.ListAPIView):
    serializer_class = HotelsListSerializer

    def get_queryset(self):
        queryset = Hotels.objects.annotate(
            average_rating=Avg('hotel_reviews__rating'),
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')
        return queryset


class HotelsDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelDetailSerializer


class HotelsReviewListAPIView(generics.ListAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = HotelsReviewFilter


class HotelsReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelReviewListSerializer


class HotelReviewCreateAPiView(generics.CreateAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelsReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hotel_review = serializer.save()
            response_serializer = HotelsReviewSerializer(hotel_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelsReviewStaticListAPIView(generics.ListAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelReviewStaticSerializers


class ReplyToHotelReviewView(generics.CreateAPIView):
    queryset = ReplyToHotelReview.objects.all()
    serializer_class = ReplyToHotelReviewSerializer


class KitchenListView(generics.ListAPIView):
    serializer_class = KitchenListSerializer

    def get_queryset(self):
        queryset = Kitchen.objects.annotate(
            average_rating=Avg('kitchen_reviews__rating'),
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')
        return queryset


class KitchenDetailView(generics.RetrieveAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenDetailSerializers


class KitchenReviewCreateAPIView(generics.CreateAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            kitchen_review = serializer.save()
            response_serializer = KitchenReviewSerializer(kitchen_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KitchenReviewListAPIView(generics.ListAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = KitchenReviewFilter


class KitchenReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewListSerializer


class KitchenReviewStaticAPIView(generics.ListAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenReviewStaticSerializers


class ReplyToKitchenReviewView(generics.CreateAPIView):
    queryset = ReplyToKitchenReview.objects.all()
    serializer_class = ReplyToKitchenReviewSerializer


class EventListAPiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = EventFilter
    search_fields = ['title']


class TicketListAPIView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializers


class CultureListAPiView(generics.ListAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializers


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializers


class NationalClothesViewSet(viewsets.ModelViewSet):
    queryset = NationalClothes.objects.all()
    serializer_class = NationalClothesSerializers


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers


class HandCraftsViewSet(viewsets.ModelViewSet):
    queryset = HandCrafts.objects.all()
    serializer_class = HandCraftsSerializers


class NationalInstrumentsViewSet(viewsets.ModelViewSet):
    queryset = NationalInstruments.objects.all()
    serializer_class = NationalInstrumentsSerializers


class CultureKitchenViewSet(viewsets.ModelViewSet):
    queryset = CultureKitchen.objects.all()
    serializer_class = CultureKitchenSerializers


class CultureKitchenMainListViewSet(viewsets.ModelViewSet):
    queryset = CultureKitchenMain.objects.all()
    serializer_class = CultureKitchenMainListSerializers


class AirLineTicketsAPIView(generics.ListAPIView):
    queryset = AirLineTickets.objects.all()
    serializer_class = AirLineTicketsSerializers


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        attractions_id = self.request.data.get('attractions')
        popular_place_id = self.request.data.get('popular_place')
        kitchen_id = self.request.data.get('kitchen')
        hotels_id = self.request.data.get('hotels')

        attractions = Attractions.objects.get(pk=attractions_id) if attractions_id else None
        popular_place = PopularPlaces.objects.get(pk=popular_place_id) if popular_place_id else None
        kitchen = Kitchen.objects.get(pk=kitchen_id) if kitchen_id else None
        hotels = Hotels.objects.get(pk=hotels_id) if hotels_id else None

        serializer.save(
            user=self.request.user,
            attractions=attractions,
            popular_place=popular_place,
            kitchen=kitchen,
            hotels=hotels
        )


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        favorite_id = self.kwargs.get('favorite_id')
        return Favorite.objects.get(id=favorite_id, user=self.request.user)



#----------------------------------

import xml.etree.ElementTree as ET
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging
from googletrans import Translator

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@staff_member_required
def upload_xml(request):
    if request.method == 'POST' and request.FILES.get('xml_file'):
        xml_file = request.FILES['xml_file']
        property_finder = PropertyFinder.objects.get_or_create(pk=1)[0]
        property_finder.file.save(xml_file.name, xml_file)

        try:
            xml_file.seek(0)
            xml_content = xml_file.read().decode('utf-8')
            logger.debug(f"XML content: {xml_content[:1000]}")
            root = ET.fromstring(xml_content)

            # PropertyFinder
            for pf_data in root.findall('property_finder'):
                if pf_data.find('file') is None:
                    logger.error("Missing tag in property_finder: file")
                    raise ValueError("Missing tag in property_finder: file")
                property_finder.file = pf_data.find('file').text
                property_finder.save()
                logger.debug(f"Processed PropertyFinder: {property_finder.file}")

            # # Region_Categoty
            # for rc_data in root.findall('region_category'):
            #     if rc_data.find('region_category') is None:
            #         logger.error("Missing tag in region_category: region_category")
            #         raise ValueError("Missing tag in region_category: region_category")
            #     category = rc_data.find('region_category').text
            #     rc, created = Region_Categoty.objects.get_or_create(region_category=category)
            #     logger.debug(f"Region_Categoty {category} {'created' if created else 'already exists'}")
            #
            # # Region
            # for r_data in root.findall('region'):
            #     required_tags = [
            #         'region_name_ru', 'region_name_en', 'region_name_ar',
            #         'region_description_ru', 'region_description_en', 'region_description_ar',
            #         'region_image', 'region_category', 'longitude', 'latitude'
            #     ]
            #     for tag in required_tags:
            #         if r_data.find(tag) is None:
            #             logger.error(f"Missing tag in region: {tag}")
            #             raise ValueError(f"Missing tag in region: {tag}")
            #     logger.debug(f"Processing region: {r_data.find('region_name_ru').text}")
            #     try:
            #         rc = Region_Categoty.objects.get(region_category=r_data.find('region_category').text)
            #     except Region_Categoty.DoesNotExist:
            #         logger.error(f"Region_Categoty not found: {r_data.find('region_category').text}")
            #         raise
            #     Region.objects.update_or_create(
            #         region_name_ru=r_data.find('region_name_ru').text,
            #         defaults={
            #             'region_name_en': r_data.find('region_name_en').text,
            #             'region_name_ar': r_data.find('region_name_ar').text,
            #             'region_description_ru': r_data.find('region_description_ru').text,
            #             'region_description_en': r_data.find('region_description_en').text,
            #             'region_description_ar': r_data.find('region_description_ar').text,
            #             'region_image': r_data.find('region_image').text,
            #             'region_category': rc,
            #             'longitude': float(r_data.find('longitude').text),
            #             'latitude': float(r_data.find('latitude').text),
            #         }
            #     )
            #     logger.debug(f"Region saved: {r_data.find('region_name_ru').text}")

            # # Home
            # for h_data in root.findall('home'):
            #     required_tags = [
            #         'home_name_ru', 'home_name_en', 'home_name_ar',
            #         'home_description_ru', 'home_description_en', 'home_description_ar',
            #         'home_image'
            #     ]
            #     for tag in required_tags:
            #         if h_data.find(tag) is None:
            #             logger.error(f"Missing tag in home: {tag}")
            #             raise ValueError(f"Missing tag in home: {tag}")
            #     Home.objects.update_or_create(
            #         home_name_ru=h_data.find('home_name_ru').text,
            #         defaults={
            #             'home_name_en': h_data.find('home_name_en').text,
            #             'home_name_ar': h_data.find('home_name_ar').text,
            #             'home_description_ru': h_data.find('home_description_ru').text,
            #             'home_description_en': h_data.find('home_description_en').text,
            #             'home_description_ar': h_data.find('home_description_ar').text,
            #             'home_image': h_data.find('home_image').text,
            #         }
            #     )
            #     logger.debug(f"Home saved: {h_data.find('home_name_ru').text}")
            #
            # # PopularPlaces
            # for pp_data in root.findall('popular_place'):
            #     required_tags = [
            #         'popular_name_ru', 'popular_name_en', 'popular_name_ar',
            #         'description_ru', 'description_en', 'description_ar',
            #         'popular_image', 'region', 'longitude', 'latitude', 'address'
            #     ]
            #     for tag in required_tags:
            #         if pp_data.find(tag) is None:
            #             logger.error(f"Missing tag in popular_place: {tag}")
            #             raise ValueError(f"Missing tag in popular_place: {tag}")
            #     region = Region.objects.get(region_name_ru=pp_data.find('region').text)
            #     PopularPlaces.objects.update_or_create(
            #         popular_name_ru=pp_data.find('popular_name_ru').text,
            #         defaults={
            #             'popular_name_en': pp_data.find('popular_name_en').text,
            #             'popular_name_ar': pp_data.find('popular_name_ar').text,
            #             'description_ru': pp_data.find('description_ru').text,
            #             'description_en': pp_data.find('description_en').text,
            #             'description_ar': pp_data.find('description_ar').text,
            #             'popular_image': pp_data.find('popular_image').text,
            #             'region': region,
            #             'longitude': float(pp_data.find('longitude').text),
            #             'latitude': float(pp_data.find('latitude').text),
            #             'address': pp_data.find('address').text,
            #         }
            #     )
            #     logger.debug(f"PopularPlaces saved: {pp_data.find('popular_name_ru').text}")
            #
            # # Attractions
            # for a_data in root.findall('attraction'):
            #     required_tags = [
            #         'attraction_name_ru', 'attraction_name_en', 'attraction_name_ar',
            #         'description_ru', 'description_en', 'description_ar',
            #         'type_attraction_ru', 'type_attraction_en', 'type_attraction_ar',
            #         'region_category', 'popular_place', 'main_image'
            #     ]
            #     for tag in required_tags:
            #         if a_data.find(tag) is None:
            #             logger.error(f"Missing tag in attraction: {tag}")
            #             raise ValueError(f"Missing tag in attraction: {tag}")
            #     rc = Region_Categoty.objects.get(region_category=a_data.find('region_category').text)
            #     pp = PopularPlaces.objects.get(popular_name_ru=a_data.find('popular_place').text)
            #     Attractions.objects.update_or_create(
            #         attraction_name_ru=a_data.find('attraction_name_ru').text,
            #         defaults={
            #             'attraction_name_en': a_data.find('attraction_name_en').text,
            #             'attraction_name_ar': a_data.find('attraction_name_ar').text,
            #             'description_ru': a_data.find('description_ru').text,
            #             'description_en': a_data.find('description_en').text,
            #             'description_ar': a_data.find('description_ar').text,
            #             'type_attraction_ru': a_data.find('type_attraction_ru').text,
            #             'type_attraction_en': a_data.find('type_attraction_en').text,
            #             'type_attraction_ar': a_data.find('type_attraction_ar').text,
            #             'region_category': rc,
            #             'main_image': a_data.find('main_image').text,
            #         }
            #     )
            #     logger.debug(f"Attractions saved: {a_data.find('attraction_name_ru').text}")
            #
            # # AttractionsImage
            # for ai_data in root.findall('attraction_image'):
            #     if ai_data.find('attraction') is None or ai_data.find('image') is None:
            #         logger.error(f"Missing tag in attraction_image: {ai_data}")
            #         raise ValueError(f"Missing tag in attraction_image")
            #     attraction = Attractions.objects.get(attraction_name_ru=ai_data.find('attraction').text)
            #     AttractionsImage.objects.update_or_create(
            #         attractions=attraction,
            #         defaults={'image': ai_data.find('image').text}
            #     )
            #     logger.debug(f"AttractionsImage saved for: {ai_data.find('attraction').text}")

            # ToTry
            for tt_data in root.findall('to_try'):
                required_tags = [
                    'to_name_ru', 'to_name_en', 'to_name_ar',
                    'first_description_ru', 'first_description_en', 'first_description_ar',
                    'second_description_ru', 'second_description_en', 'second_description_ar',
                    'image', 'region'
                ]
                for tag in required_tags:
                    if tt_data.find(tag) is None:
                        logger.error(f"Missing tag in to_try: {tag}")
                        raise ValueError(f"Missing tag in to_try: {tag}")
                region = Region.objects.get(region_name_ru=tt_data.find('region').text)
                ToTry.objects.update_or_create(
                    to_name_ru=tt_data.find('to_name_ru').text,
                    defaults={
                        'to_name_en': tt_data.find('to_name_en').text,
                        'to_name_ar': tt_data.find('to_name_ar').text,
                        'first_description_ru': tt_data.find('first_description_ru').text,
                        'first_description_en': tt_data.find('first_description_en').text,
                        'first_description_ar': tt_data.find('first_description_ar').text,
                        'second_description_ru': tt_data.find('second_description_ru').text,
                        'second_description_en': tt_data.find('second_description_en').text,
                        'second_description_ar': tt_data.find('second_description_ar').text,
                        'image': tt_data.find('image').text,
                        'region': region,
                    }
                )
                logger.debug(f"ToTry saved: {tt_data.find('to_name_ru').text}")

            # Hotels
            for h_data in root.findall('hotel'):
                required_tags = [
                    'name_ru', 'name_en', 'name_ar',
                    'description_ru', 'description_en', 'description_ar',
                    'address_ru', 'address_en', 'address_ar',
                    'main_image', 'region', 'popular_places', 'bedroom', 'bathroom',
                    'cars', 'bikes', 'pets', 'price_short_period', 'price_medium_period',
                    'price_long_period', 'longitude', 'latitude', 'contact'
                ]
                for tag in required_tags:
                    if h_data.find(tag) is None:
                        logger.error(f"Missing tag in hotel: {tag}")
                        raise ValueError(f"Missing tag in hotel: {tag}")
                rc = Region_Categoty.objects.get(region_category=h_data.find('region').text)
                pp = PopularPlaces.objects.get(popular_name_ru=h_data.find('popular_places').text)
                Hotels.objects.update_or_create(
                    name_ru=h_data.find('name_ru').text,
                    defaults={
                        'name_en': h_data.find('name_en').text,
                        'name_ar': h_data.find('name_ar').text,
                        'description_ru': h_data.find('description_ru').text,
                        'description_en': h_data.find('description_en').text,
                        'description_ar': h_data.find('description_ar').text,
                        'address_ru': h_data.find('address_ru').text,
                        'address_en': h_data.find('address_en').text,
                        'address_ar': h_data.find('address_ar').text,
                        'main_image': h_data.find('main_image').text,
                        'region': rc,
                        'popular_places': pp,
                        'bedroom': int(h_data.find('bedroom').text),
                        'bathroom': int(h_data.find('bathroom').text),
                        'cars': int(h_data.find('cars').text),
                        'bikes': int(h_data.find('bikes').text),
                        'pets': int(h_data.find('pets').text),
                        'price_short_period': int(h_data.find('price_short_period').text),
                        'price_medium_period': int(h_data.find('price_medium_period').text),
                        'price_long_period': int(h_data.find('price_long_period').text),
                        'longitude': float(h_data.find('longitude').text),
                        'latitude': float(h_data.find('latitude').text),
                        'contact': h_data.find('contact').text,
                    }
                )
                logger.debug(f"Hotel saved: {h_data.find('name_ru').text}")

            # Amenities
            for am_data in root.findall('amenity'):
                required_tags = ['hotel', 'amenity_ru', 'amenity_en', 'amenity_ar', 'icon']
                for tag in required_tags:
                    if am_data.find(tag) is None:
                        logger.error(f"Missing tag in amenity: {tag}")
                        raise ValueError(f"Missing tag in amenity: {tag}")
                hotel = Hotels.objects.get(name_ru=am_data.find('hotel').text)
                Amenities.objects.update_or_create(
                    hotel=hotel,
                    amenity_ru=am_data.find('amenity_ru').text,
                    defaults={
                        'amenity_en': am_data.find('amenity_en').text,
                        'amenity_ar': am_data.find('amenity_ar').text,
                        'icon': am_data.find('icon').text,
                    }
                )
                logger.debug(f"Amenity saved for hotel: {am_data.find('hotel').text}")

            # SafetyAndHygiene
            for sh_data in root.findall('safety_and_hygiene'):
                required_tags = ['hotel', 'name_ru', 'name_en', 'name_ar']
                for tag in required_tags:
                    if sh_data.find(tag) is None:
                        logger.error(f"Missing tag in safety_and_hygiene: {tag}")
                        raise ValueError(f"Missing tag in safety_and_hygiene: {tag}")
                hotel = Hotels.objects.get(name_ru=sh_data.find('hotel').text)
                SafetyAndHygiene.objects.update_or_create(
                    hotel=hotel,
                    name_ru=sh_data.find('name_ru').text,
                    defaults={
                        'name_en': sh_data.find('name_en').text,
                        'name_ar': sh_data.find('name_ar').text,
                    }
                )
                logger.debug(f"SafetyAndHygiene saved for hotel: {sh_data.find('hotel').text}")

            # HotelsImage
            for hi_data in root.findall('hotel_image'):
                if hi_data.find('hotel') is None or hi_data.find('image') is None:
                    logger.error(f"Missing tag in hotel_image: {hi_data}")
                    raise ValueError(f"Missing tag in hotel_image")
                hotel = Hotels.objects.get(name_ru=hi_data.find('hotel').text)
                HotelsImage.objects.update_or_create(
                    hotel=hotel,
                    defaults={'image': hi_data.find('image').text}
                )
                logger.debug(f"HotelImage saved for hotel: {hi_data.find('hotel').text}")

            # Kitchen
            for k_data in root.findall('kitchen'):
                required_tags = [
                    'kitchen_name_ru', 'kitchen_name_en', 'kitchen_name_ar',
                    'description_ru', 'description_en', 'description_ar',
                    'specialized_menu_ru', 'specialized_menu_en', 'specialized_menu_ar',
                    'main_image', 'kitchen_region', 'popular_places', 'price',
                    'meal_time', 'type_of_cafe'
                ]
                for tag in required_tags:
                    if k_data.find(tag) is None:
                        logger.error(f"Missing tag in kitchen: {tag}")
                        raise ValueError(f"Missing tag in kitchen: {tag}")
                rc = Region_Categoty.objects.get(region_category=k_data.find('kitchen_region').text)
                pp = PopularPlaces.objects.get(popular_name_ru=k_data.find('popular_places').text)
                Kitchen.objects.update_or_create(
                    kitchen_name_ru=k_data.find('kitchen_name_ru').text,
                    defaults={
                        'kitchen_name_en': k_data.find('kitchen_name_en').text,
                        'kitchen_name_ar': k_data.find('kitchen_name_ar').text,
                        'description_ru': k_data.find('description_ru').text,
                        'description_en': k_data.find('description_en').text,
                        'description_ar': k_data.find('description_ar').text,
                        'specialized_menu_ru': k_data.find('specialized_menu_ru').text,
                        'specialized_menu_en': k_data.find('specialized_menu_en').text,
                        'specialized_menu_ar': k_data.find('specialized_menu_ar').text,
                        'main_image': k_data.find('main_image').text,
                        'kitchen_region': rc,
                        'popular_places': pp,
                        'price': int(k_data.find('price').text),
                        'meal_time': k_data.find('meal_time').text,
                        'type_of_cafe': k_data.find('type_of_cafe').text,
                    }
                )
                logger.debug(f"Kitchen saved: {k_data.find('kitchen_name_ru').text}")

            # KitchenLocation
            for kl_data in root.findall('kitchen_location'):
                required_tags = [
                    'kitchen', 'address_ru', 'address_en', 'address_ar',
                    'website', 'email', 'phone_number', 'longitude', 'latitude'
                ]
                for tag in required_tags:
                    if kl_data.find(tag) is None:
                        logger.error(f"Missing tag in kitchen_location: {tag}")
                        raise ValueError(f"Missing tag in kitchen_location: {tag}")
                kitchen = Kitchen.objects.get(kitchen_name_ru=kl_data.find('kitchen').text)
                KitchenLocation.objects.update_or_create(
                    kitchen=kitchen,
                    defaults={
                        'address_ru': kl_data.find('address_ru').text,
                        'address_en': kl_data.find('address_en').text,
                        'address_ar': kl_data.find('address_ar').text,
                        'website': kl_data.find('website').text,
                        'email': kl_data.find('email').text,
                        'phone_number': kl_data.find('phone_number').text,
                        'longitude': float(kl_data.find('longitude').text),
                        'latitude': float(kl_data.find('latitude').text),
                    }
                )
                logger.debug(f"KitchenLocation saved for: {kl_data.find('kitchen').text}")

            # KitchenImage
            for ki_data in root.findall('kitchen_image'):
                if ki_data.find('kitchen') is None or ki_data.find('image') is None:
                    logger.error(f"Missing tag in kitchen_image: {ki_data}")
                    raise ValueError(f"Missing tag in kitchen_image")
                kitchen = Kitchen.objects.get(kitchen_name_ru=ki_data.find('kitchen').text)
                KitchenImage.objects.update_or_create(
                    kitchen=kitchen,
                    defaults={'image': ki_data.find('image').text}
                )
                logger.debug(f"KitchenImage saved for: {ki_data.find('kitchen').text}")

            # EventCategories
            for ec_data in root.findall('event_category'):
                if ec_data.find('category') is None:
                    logger.error("Missing tag in event_category: category")
                    raise ValueError("Missing tag in event_category: category")
                EventCategories.objects.get_or_create(
                    category=ec_data.find('category').text
                )
                logger.debug(f"EventCategory saved: {ec_data.find('category').text}")

            # Event
            # for e_data in root.findall('event'):
            #     required_tags = ['category', 'image', 'popular_places', 'title', 'date', 'time', 'address', 'price', 'ticket']
            #     for tag in required_tags:
            #         if e_data.find(tag) is None:
            #             logger.error(f"Missing tag in event: {tag}")
            #             raise ValueError(f"Missing tag in event: {tag}")
            #     category = EventCategories.objects.get(category=e_data.find('concert').text)
            #     pp = PopularPlaces.objects.get(popular_name_ru=e_data.find('popular_places').text)
            #     Event.objects.update_or_create(
            #         title=e_data.find('title').text,
            #         defaults={
            #             'category': category,
            #             'image': e_data.find('image').text,
            #             'popular_places': pp,
            #             'date': e_data.find('date').text,
            #             'time': e_data.find('time').text,
            #             'address': e_data.find('address').text,
            #             'price': int(e_data.find('price').text),
            #             'ticket': e_data.find('ticket').text.lower() == 'true',
            #         }
            #     )
            #     logger.debug(f"Event saved: {e_data.find('title').text}")

            # Ticket
            # for t_data in root.findall('ticket'):
            #     required_tags = ['concert', 'image', 'title', 'date', 'time', 'address', 'price']
            #     for tag in required_tags:
            #         if t_data.find(tag) is None:
            #             logger.error(f"Missing tag in ticket: {tag}")
            #             raise ValueError(f"Missing tag in ticket: {tag}")
            #     category = EventCategories.objects.get(category=e_data.find('concert').text)
            #     Ticket.objects.update_or_create(
            #         title=t_data.find('title').text,
            #         defaults={
            #             'concert': category,
            #             'image': t_data.find('image').text,
            #             'date': t_data.find('date').text,
            #             'time': t_data.find('time').text,
            #             'address': t_data.find('address').text,
            #             'price': int(t_data.find('price').text),
            #         }
            #     )
            #     logger.debug(f"Ticket saved: {t_data.find('title').text}")

            # CultureCategory
            for cc_data in root.findall('culture_category'):
                if cc_data.find('culture_name') is None:
                    logger.error("Missing tag in culture_category: culture_name")
                    raise ValueError("Missing tag in culture_category: culture_name")
                CultureCategory.objects.get_or_create(
                    culture_name=cc_data.find('culture_name').text
                )
                logger.debug(f"CultureCategory saved: {cc_data.find('culture_name').text}")

            # Culture
            for c_data in root.findall('culture'):
                required_tags = [
                    'culture_name_ru', 'culture_name_en', 'culture_name_ar',
                    'culture_description_ru', 'culture_description_en', 'culture_description_ar',
                    'culture_image', 'culture'
                ]
                for tag in required_tags:
                    if c_data.find(tag) is None:
                        logger.error(f"Missing tag in culture: {tag}")
                        raise ValueError(f"Missing tag in culture: {tag}")
                cc = CultureCategory.objects.get(culture_name=c_data.find('culture').text)
                Culture.objects.update_or_create(
                    culture_name_ru=c_data.find('culture_name_ru').text,
                    defaults={
                        'culture_name_en': c_data.find('culture_name_en').text,
                        'culture_name_ar': c_data.find('culture_name_ar').text,
                        'culture_description_ru': c_data.find('culture_description_ru').text,
                        'culture_description_en': c_data.find('culture_description_en').text,
                        'culture_description_ar': c_data.find('culture_description_ar').text,
                        'culture_image': c_data.find('culture_image').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"Culture saved: {c_data.find('culture_name_ru').text}")

            # Games
            for g_data in root.findall('game'):
                required_tags = [
                    'games_name_ru', 'games_name_en', 'games_name_ar',
                    'games_description_ru', 'games_description_en', 'games_description_ar',
                    'games_image', 'culture'
                ]
                for tag in required_tags:
                    if g_data.find(tag) is None:
                        logger.error(f"Missing tag in game: {tag}")
                        raise ValueError(f"Missing tag in game: {tag}")
                cc = CultureCategory.objects.get(culture_name=g_data.find('culture').text)
                Games.objects.update_or_create(
                    games_name_ru=g_data.find('games_name_ru').text,
                    defaults={
                        'games_name_en': g_data.find('games_name_en').text,
                        'games_name_ar': g_data.find('games_name_ar').text,
                        'games_description_ru': g_data.find('games_description_ru').text,
                        'games_description_en': g_data.find('games_description_en').text,
                        'games_description_ar': g_data.find('games_description_ar').text,
                        'games_image': g_data.find('games_image').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"Game saved: {g_data.find('games_name_ru').text}")

            # NationalClothes
            for nc_data in root.findall('national_clothes'):
                required_tags = [
                    'clothes_name_ru', 'clothes_name_en', 'clothes_name_ar',
                    'clothes_description_ru', 'clothes_description_en', 'clothes_description_ar',
                    'clothes_image', 'culture'
                ]
                for tag in required_tags:
                    if nc_data.find(tag) is None:
                        logger.error(f"Missing tag in national_clothes: {tag}")
                        raise ValueError(f"Missing tag in national_clothes: {tag}")
                cc = CultureCategory.objects.get(culture_name=nc_data.find('culture').text)
                NationalClothes.objects.update_or_create(
                    clothes_name_ru=nc_data.find('clothes_name_ru').text,
                    defaults={
                        'clothes_name_en': nc_data.find('clothes_name_en').text,
                        'clothes_name_ar': nc_data.find('clothes_name_ar').text,
                        'clothes_description_ru': nc_data.find('clothes_description_ru').text,
                        'clothes_description_en': nc_data.find('clothes_description_en').text,
                        'clothes_description_ar': nc_data.find('clothes_description_ar').text,
                        'clothes_image': nc_data.find('clothes_image').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"NationalClothes saved: {nc_data.find('clothes_name_ru').text}")

            # HandCrafts
            for hc_data in root.findall('hand_craft'):
                required_tags = [
                    'hand_name_ru', 'hand_name_en', 'hand_name_ar',
                    'hand_description_ru', 'hand_description_en', 'hand_description_ar',
                    'hand_image', 'culture'
                ]
                for tag in required_tags:
                    if hc_data.find(tag) is None:
                        logger.error(f"Missing tag in hand_craft: {tag}")
                        raise ValueError(f"Missing tag in hand_craft: {tag}")
                cc = CultureCategory.objects.get(culture_name=hc_data.find('culture').text)
                HandCrafts.objects.update_or_create(
                    hand_name_ru=hc_data.find('hand_name_ru').text,
                    defaults={
                        'hand_name_en': hc_data.find('hand_name_en').text,
                        'hand_name_ar': hc_data.find('hand_name_ar').text,
                        'hand_description_ru': hc_data.find('hand_description_ru').text,
                        'hand_description_en': hc_data.find('hand_description_en').text,
                        'hand_description_ar': hc_data.find('hand_description_ar').text,
                        'hand_image': hc_data.find('hand_image').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"HandCrafts saved: {hc_data.find('hand_name_ru').text}")

            # Currency
            for c_data in root.findall('currency'):
                required_tags = ['currency_name_ru', 'currency_name_en', 'currency_name_ar', 'culture']
                for tag in required_tags:
                    if c_data.find(tag) is None:
                        logger.error(f"Missing tag in currency: {tag}")
                        raise ValueError(f"Missing tag in currency: {tag}")
                Currency.objects.get_or_create(
                    currency_name_ru=c_data.find('currency_name_ru').text,
                    defaults={
                        'currency_name_en': c_data.find('currency_name_en').text,
                        'currency_name_ar': c_data.find('currency_name_ar').text,
                        'culture': c_data.find('culture').text,
                    }
                )
                logger.debug(f"Currency saved: {c_data.find('currency_name_ru').text}")

            # Currency_Description
            for cd_data in root.findall('currency_description'):
                required_tags = ['currency', 'description_ru', 'description_en', 'description_ar']
                for tag in required_tags:
                    if cd_data.find(tag) is None:
                        logger.error(f"Missing tag in currency_description: {tag}")
                        raise ValueError(f"Missing tag in currency_description: {tag}")
                currency = Currency.objects.get(currency_name_ru=cd_data.find('currency').text)
                Currency_Description.objects.update_or_create(
                    currency=currency,
                    defaults={
                        'description_ru': cd_data.find('description_ru').text,
                        'description_en': cd_data.find('description_en').text,
                        'description_ar': cd_data.find('description_ar').text,
                    }
                )
                logger.debug(f"Currency_Description saved for: {cd_data.find('currency').text}")

            # Currency_Image
            for ci_data in root.findall('currency_image'):
                required_tags = ['currency', 'front_image', 'back_image']
                for tag in required_tags:
                    if ci_data.find(tag) is None:
                        logger.error(f"Missing tag in currency_image: {tag}")
                        raise ValueError(f"Missing tag in currency_image: {tag}")
                currency = Currency.objects.get(currency_name_ru=ci_data.find('currency').text)
                Currency_Image.objects.update_or_create(
                    currency=currency,
                    defaults={
                        'front_image': ci_data.find('front_image').text,
                        'back_image': ci_data.find('back_image').text,
                    }
                )
                logger.debug(f"Currency_Image saved for: {ci_data.find('currency').text}")

            # NationalInstruments
            for ni_data in root.findall('national_instrument'):
                required_tags = [
                    'national_name_ru', 'national_name_en', 'national_name_ar',
                    'national_description_ru', 'national_description_en', 'national_description_ar',
                    'national_image', 'culture'
                ]
                for tag in required_tags:
                    if ni_data.find(tag) is None:
                        logger.error(f"Missing tag in national_instrument: {tag}")
                        raise ValueError(f"Missing tag in national_instrument: {tag}")
                cc = CultureCategory.objects.get(culture_name=ni_data.find('culture').text)
                NationalInstruments.objects.update_or_create(
                    national_name_ru=ni_data.find('national_name_ru').text,
                    defaults={
                        'national_name_en': ni_data.find('national_name_en').text,
                        'national_name_ar': ni_data.find('national_name_ar').text,
                        'national_description_ru': ni_data.find('national_description_ru').text,
                        'national_description_en': ni_data.find('national_description_en').text,
                        'national_description_ar': ni_data.find('national_description_ar').text,
                        'national_image': ni_data.find('national_image').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"NationalInstruments saved: {ni_data.find('national_name_ru').text}")

            # CultureKitchen
            for ck_data in root.findall('culture_kitchen'):
                required_tags = [
                    'kitchen_name_ru', 'kitchen_name_en', 'kitchen_name_ar',
                    'kitchen_description_ru', 'kitchen_description_en', 'kitchen_description_ar',
                    'culture'
                ]
                for tag in required_tags:
                    if ck_data.find(tag) is None:
                        logger.error(f"Missing tag in culture_kitchen: {tag}")
                        raise ValueError(f"Missing tag in culture_kitchen: {tag}")
                cc = CultureCategory.objects.get(culture_name=ck_data.find('culture').text)
                CultureKitchen.objects.update_or_create(
                    kitchen_name_ru=ck_data.find('kitchen_name_ru').text,
                    defaults={
                        'kitchen_name_en': ck_data.find('kitchen_name_en').text,
                        'kitchen_name_ar': ck_data.find('kitchen_name_ar').text,
                        'kitchen_description_ru': ck_data.find('kitchen_description_ru').text,
                        'kitchen_description_en': ck_data.find('kitchen_description_en').text,
                        'kitchen_description_ar': ck_data.find('kitchen_description_ar').text,
                        'culture': cc,
                    }
                )
                logger.debug(f"CultureKitchen saved: {ck_data.find('kitchen_name_ru').text}")

            # CultureKitchenImage
            for cki_data in root.findall('culture_kitchen_image'):
                if cki_data.find('culture_kitchen') is None or cki_data.find('image') is None:
                    logger.error(f"Missing tag in culture_kitchen_image: {cki_data}")
                    raise ValueError(f"Missing tag in culture_kitchen_image")
                ck = CultureKitchen.objects.get(kitchen_name_ru=cki_data.find('culture_kitchen').text)
                CultureKitchenImage.objects.update_or_create(
                    culture_kitchen=ck,
                    defaults={'image': cki_data.find('image').text}
                )
                logger.debug(f"CultureKitchenImage saved for: {cki_data.find('culture_kitchen').text}")

            # CultureKitchenMain
            for ckm_data in root.findall('culture_kitchen_main'):
                required_tags = [
                    'title_ru', 'title_en', 'title_ar',
                    'description_ru', 'description_en', 'description_ar',
                    'culture', 'image_1', 'image_2', 'image_3', 'image_4'
                ]
                for tag in required_tags:
                    if ckm_data.find(tag) is None:
                        logger.error(f"Missing tag in culture_kitchen_main: {tag}")
                        raise ValueError(f"Missing tag in culture_kitchen_main: {tag}")
                cc = CultureCategory.objects.get(culture_name=ckm_data.find('culture').text)
                CultureKitchenMain.objects.update_or_create(
                    title_ru=ckm_data.find('title_ru').text,
                    defaults={
                        'title_en': ckm_data.find('title_en').text,
                        'title_ar': ckm_data.find('title_ar').text,
                        'description_ru': ckm_data.find('description_ru').text,
                        'description_en': ckm_data.find('description_en').text,
                        'description_ar': ckm_data.find('description_ar').text,
                        'culture': cc,
                        'image_1': ckm_data.find('image_1').text,
                        'image_2': ckm_data.find('image_2').text,
                        'image_3': ckm_data.find('image_3').text,
                        'image_4': ckm_data.find('image_4').text,
                    }
                )
                logger.debug(f"CultureKitchenMain saved: {ckm_data.find('title_ru').text}")

            # AirLineTickets
            for at_data in root.findall('airline_ticket'):
                required_tags = [
                    'name_ru', 'name_en', 'name_ar',
                    'description_ru', 'description_en', 'description_ar',
                    'logo', 'website'
                ]
                for tag in required_tags:
                    if at_data.find(tag) is None:
                        logger.error(f"Missing tag in airline_ticket: {tag}")
                        raise ValueError(f"Missing tag in airline_ticket: {tag}")
                AirLineTickets.objects.update_or_create(
                    name_ru=at_data.find('name_ru').text,
                    defaults={
                        'name_en': at_data.find('name_en').text,
                        'name_ar': at_data.find('name_ar').text,
                        'description_ru': at_data.find('description_ru').text,
                        'description_en': at_data.find('description_en').text,
                        'description_ar': at_data.find('description_ar').text,
                        'logo': at_data.find('logo').text,
                        'website': at_data.find('website').text,
                    }
                )
                logger.debug(f"AirLineTickets saved: {at_data.find('name_ru').text}")

            # AirLineDirections
            for ad_data in root.findall('airline_direction'):
                required_tags = ['ticket', 'directions_ru', 'directions_en', 'directions_ar']
                for tag in required_tags:
                    if ad_data.find(tag) is None:
                        logger.error(f"Missing tag in airline_direction: {tag}")
                        raise ValueError(f"Missing tag in airline_direction: {tag}")
                ticket = AirLineTickets.objects.get(name_ru=ad_data.find('ticket').text)
                AirLineDirections.objects.update_or_create(
                    ticket=ticket,
                    directions_ru=ad_data.find('directions_ru').text,
                    defaults={
                        'directions_en': ad_data.find('directions_en').text,
                        'directions_ar': ad_data.find('directions_ar').text,
                    }
                )
                logger.debug(f"AirLineDirections saved for: {ad_data.find('ticket').text}")

            messages.success(request, "Данные из XML успешно импортированы.")
        except ET.ParseError as e:
            logger.error(f"ParseError: {e}")
            messages.error(request, f"Неверный формат XML-файла: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            messages.error(request, f"Ошибка при обработке XML: {str(e)}")

        return redirect('admin:country_propertyfinder_changelist')

    messages.error(request, "Файл не загружен.")
    return redirect('admin:country_propertyfinder_changelist')