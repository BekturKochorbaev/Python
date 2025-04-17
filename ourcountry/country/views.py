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
                property_finder.file = pf_data.find('file').text
                property_finder.save()

            # Region_Categoty
            for rc_data in root.findall('region_category'):
                Region_Categoty.objects.get_or_create(
                    region_category=rc_data.find('region_category').text
                )

            # Region
            for r_data in root.findall('region'):
                rc_name = r_data.find('region_category').text
                rc = Region_Categoty.objects.get(region_category=rc_name)
                Region.objects.update_or_create(
                    region_name=r_data.find('region_name').text,
                    defaults={
                        'region_image': r_data.find('region_image').text,
                        'region_description': r_data.find('region_description').text,
                        'region_category': rc,
                        'longitude': float(r_data.find('longitude').text),
                        'latitude': float(r_data.find('latitude').text),
                    }
                )

            # Home
            for h_data in root.findall('home'):
                Home.objects.update_or_create(
                    home_name=h_data.find('home_name').text,
                    defaults={
                        'home_image': h_data.find('home_image').text,
                        'home_description': h_data.find('home_description').text,
                    }
                )

            # PopularPlaces
            for pp_data in root.findall('popular_place'):
                region = Region.objects.get(region_name=pp_data.find('region').text)
                PopularPlaces.objects.update_or_create(
                    popular_name=pp_data.find('popular_name').text,
                    region=region,
                    defaults={
                        'popular_image': pp_data.find('popular_image').text,
                        'description': pp_data.find('description').text,
                        'longitude': float(pp_data.find('longitude').text),
                        'latitude': float(pp_data.find('latitude').text),
                        'address': pp_data.find('address').text,
                    }
                )

            # Attractions
            for a_data in root.findall('attraction'):
                rc = Region_Categoty.objects.get(region_category=a_data.find('region_category').text)
                Attractions.objects.update_or_create(
                    attraction_name=a_data.find('attraction_name').text,
                    defaults={
                        'description': a_data.find('description').text,
                        'region_category': rc,
                        'main_image': a_data.find('main_image').text,
                        'type_attraction': a_data.find('type_attraction').text,
                    }
                )

                # Kitchen
            for k_data in root.findall('kitchen'):
                    rc = Region_Categoty.objects.get(region_category=k_data.find('kitchen_region').text)
                    pp = PopularPlaces.objects.get(popular_name=k_data.find('popular_places').text)
                    Kitchen.objects.update_or_create(
                        kitchen_name=k_data.find('kitchen_name').text,
                        defaults={
                            'description': k_data.find('description').text,
                            'main_image': k_data.find('main_image').text,
                            'kitchen_region': rc,
                            'popular_places': pp,
                            'price': int(k_data.find('price').text),
                            'specialized_menu': k_data.find('specialized_menu').text,
                            'meal_time': k_data.find('meal_time').text.split(','),
                            'type_of_cafe': k_data.find('type_of_cafe').text.split(','),
                        }
                    )

                # KitchenLocation
            for kl_data in root.findall('kitchen_location'):
                    kitchen = Kitchen.objects.get(kitchen_name=kl_data.find('kitchen').text)
                    KitchenLocation.objects.update_or_create(
                        kitchen=kitchen,
                        defaults={
                            'address': kl_data.find('address').text,
                            'website': kl_data.find('website').text,
                            'email': kl_data.find('email').text,
                            'phone_number': kl_data.find('phone_number').text,
                            'longitude': kl_data.find('longitude').text,
                            'latitude': kl_data.find('latitude').text,
                        }
                    )

                # KitchenImage
            for ki_data in root.findall('kitchen_image'):
                    kitchen = Kitchen.objects.get(kitchen_name=ki_data.find('kitchen').text)
                    KitchenImage.objects.update_or_create(
                        kitchen=kitchen,
                        defaults={'image': ki_data.find('image').text}
                    )

                    # EventCategories

            for ec_data in root.findall('event_category'):
                        EventCategories.objects.get_or_create(
                            category=ec_data.find('category').text
                        )

                    # Event
            for e_data in root.findall('event'):
                        category = EventCategories.objects.get(category=e_data.find('category').text)
                        pp = PopularPlaces.objects.get(popular_name=e_data.find('popular_places').text)
                        Event.objects.update_or_create(
                            title=e_data.find('title').text,
                            defaults={
                                'category': category,
                                'image': e_data.find('image').text,
                                'popular_places': pp,
                                'date': e_data.find('date').text,
                                'time': e_data.find('time').text,
                                'address': e_data.find('address').text,
                                'price': int(e_data.find('price').text),
                                'ticket': e_data.find('ticket').text.lower() == 'true',
                            }
                        )

                    # Ticket
            for t_data in root.findall('ticket'):
                        concert = EventCategories.objects.get(category=t_data.find('concert').text)
                        Ticket.objects.update_or_create(
                            title=t_data.find('title').text,
                            defaults={
                                'concert': concert,
                                'image': t_data.find('image').text,
                                'date': t_data.find('date').text,
                                'time': t_data.find('time').text,
                                'address': t_data.find('address').text,
                                'price': int(t_data.find('price').text),
                            }
                        )

                    # CultureCategory
            for cc_data in root.findall('culture_category'):
                        CultureCategory.objects.get_or_create(
                            culture_name=cc_data.find('culture_name').text
                        )

                    # Culture
            for c_data in root.findall('culture'):
                        culture = CultureCategory.objects.get(culture_name=c_data.find('culture').text)
                        Culture.objects.update_or_create(
                            culture_name=c_data.find('culture_name').text,
                            defaults={
                                'culture_description': c_data.find('culture_description').text,
                                'culture_image': c_data.find('culture_image').text,
                                'culture': culture,
                            }
                        )

                    # Games
            for g_data in root.findall('game'):
                        culture = CultureCategory.objects.get(culture_name=g_data.find('culture').text)
                        Games.objects.update_or_create(
                            games_name=g_data.find('games_name').text,
                            defaults={
                                'games_description': g_data.find('games_description').text,
                                'games_image': g_data.find('games_image').text,
                                'culture': culture,
                            }
                        )

                    # NationalClothes
            for nc_data in root.findall('national_clothes'):
                        culture = CultureCategory.objects.get(culture_name=nc_data.find('culture').text)
                        NationalClothes.objects.update_or_create(
                            clothes_name=nc_data.find('clothes_name').text,
                            defaults={
                                'clothes_description': nc_data.find('clothes_description').text,
                                'clothes_image': nc_data.find('clothes_image').text,
                                'culture': culture,
                            }
                        )

                    # HandCrafts
            for hc_data in root.findall('hand_craft'):
                        culture = CultureCategory.objects.get(culture_name=hc_data.find('culture').text)
                        HandCrafts.objects.update_or_create(
                            hand_name=hc_data.find('hand_name').text,
                            defaults={
                                'hand_description': hc_data.find('hand_description').text,
                                'hand_image': hc_data.find('hand_image').text,
                                'culture': culture,
                            }
                        )

                    # Currency
            for c_data in root.findall('currency'):
                        culture = CultureCategory.objects.get(culture_name=c_data.find('culture').text)
                        Currency.objects.update_or_create(
                            currency_name=c_data.find('currency_name').text,
                            defaults={'culture': culture}
                        )

                    # Currency_Description
            for cd_data in root.findall('currency_description'):
                        currency = Currency.objects.get(currency_name=cd_data.find('currency').text)
                        Currency_Description.objects.update_or_create(
                            currency=currency,
                            defaults={'description': cd_data.find('description').text}
                        )

                    # Currency_Image
            for ci_data in root.findall('currency_image'):
                        currency = Currency.objects.get(currency_name=ci_data.find('currency').text)
                        Currency_Image.objects.update_or_create(
                            currency=currency,
                            defaults={
                                'front_image': ci_data.find('front_image').text,
                                'back_image': ci_data.find('back_image').text,
                            }
                        )

                    # NationalInstruments
            for ni_data in root.findall('national_instrument'):
                        culture = CultureCategory.objects.get(culture_name=ni_data.find('culture').text)
                        NationalInstruments.objects.update_or_create(
                            national_name=ni_data.find('national_name').text,
                            defaults={
                                'national_description': ni_data.find('national_description').text,
                                'national_image': ni_data.find('national_image').text,
                                'culture': culture,
                            }
                        )

                    # CultureKitchen
            for ck_data in root.findall('culture_kitchen'):
                        culture = CultureCategory.objects.get(culture_name=ck_data.find('culture').text)
                        CultureKitchen.objects.update_or_create(
                            kitchen_name=ck_data.find('kitchen_name').text,
                            defaults={
                                'kitchen_description': ck_data.find('kitchen_description').text,
                                'culture': culture,
                            }
                        )

                    # CultureKitchenImage
            for cki_data in root.findall('culture_kitchen_image'):
                        culture_kitchen = CultureKitchen.objects.get(kitchen_name=cki_data.find('culture_kitchen').text)
                        CultureKitchenImage.objects.update_or_create(
                            culture_kitchen=culture_kitchen,
                            defaults={'image': cki_data.find('image').text}
                        )

                    # CultureKitchenMain
            for ckm_data in root.findall('culture_kitchen_main'):
                        culture = CultureCategory.objects.get(culture_name=ckm_data.find('culture').text)
                        CultureKitchenMain.objects.update_or_create(
                            title=ckm_data.find('title').text,
                            defaults={
                                'description': ckm_data.find('description').text,
                                'culture': culture,
                                'image_1': ckm_data.find('image_1').text,
                                'image_2': ckm_data.find('image_2').text,
                                'image_3': ckm_data.find('image_3').text,
                                'image_4': ckm_data.find('image_4').text,
                            }
                        )


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