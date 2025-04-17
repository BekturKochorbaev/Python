from .models import (Region, Home, Attractions, PopularPlaces, ToTry, Hotels, Kitchen,
                     Culture, Games, NationalClothes, HandCrafts, Currency, NationalInstruments,
                     CultureKitchen, KitchenLocation, Currency_Description, Amenities, SafetyAndHygiene,
                     CultureKitchenMain, AirLineTickets, AirLineDirections, )
from modeltranslation.translator import TranslationOptions, register


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name', 'region_description')


@register(Home)
class HomeTranslationOptions(TranslationOptions):
    fields = ('home_name', 'home_description')


@register(Attractions)
class AttractionsTranslationOptions(TranslationOptions):
    fields = ('attraction_name', 'description', 'type_attraction')


@register(PopularPlaces)
class PopularPlacesTranslationOptions(TranslationOptions):
    fields = ('popular_name', 'description',)


@register(ToTry)
class ToTryTranslationOptions(TranslationOptions):
    fields = ('to_name', 'first_description', 'second_description')


@register(Hotels)
class HotelsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'address')


@register(Kitchen)
class KitchenTranslationOptions(TranslationOptions):
    fields = ('kitchen_name', 'description', 'specialized_menu')


@register(KitchenLocation)
class KitchenLocationTranslationOptions(TranslationOptions):
    fields = ('address',)


@register(Culture)
class CultureTranslationOptions(TranslationOptions):
    fields = ('culture_name', 'culture_description')


@register(Games)
class GamesTranslationOptions(TranslationOptions):
    fields = ('games_name', 'games_description')


@register(NationalClothes)
class NationalClothesTranslationOptions(TranslationOptions):
    fields = ('clothes_name', 'clothes_description')


@register(HandCrafts)
class HandCraftsTranslationOptions(TranslationOptions):
    fields = ('hand_name', 'hand_description')


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('currency_name',)


@register(Currency_Description)
class Currency_DescriptionTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(NationalInstruments)
class CultureTranslationOptions(TranslationOptions):
    fields = ('national_name', 'national_description')


@register(CultureKitchen)
class CultureTranslationOptions(TranslationOptions):
    fields = ('kitchen_name', 'kitchen_description')


@register(Amenities)
class AmenitiesTranslationOptions(TranslationOptions):
    fields = ('amenity',)


@register(SafetyAndHygiene)
class SafetyAndHygieneTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(CultureKitchenMain)
class CultureKitchenMainTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AirLineTickets)
class AirLineTicketsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(AirLineDirections)
class AirLineDirectionsTranslationOptions(TranslationOptions):
    fields = ('directions',)





