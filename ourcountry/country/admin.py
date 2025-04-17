from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
from django.contrib.auth.models import Group
from accounts.models import UserProfile
from .models import (
    Region, Home, PopularPlaces, ToTry, Culture, Games, NationalClothes, HandCrafts,
    NationalInstruments, CultureKitchenImage, CultureKitchen, Attractions, AttractionsImage, HotelsImage, Amenities,
    SafetyAndHygiene, Hotels, KitchenLocation, KitchenImage, Kitchen, EventCategories, Event, CultureCategory,
    Region_Categoty, Ticket, Currency_Description, Currency_Image, Currency, CultureKitchenMain,
    AirLineDirections, AirLineTickets, KitchenReview, PropertyFinder
)

from django.urls import reverse
from django.utils.html import format_html


@admin.register(PropertyFinder)
class PropertyFinderAdmin(admin.ModelAdmin):
    list_display = ['file', 'upload_xml_button']

    def upload_xml_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Загрузить XML</a>',
            reverse('country:xml')
        )

    upload_xml_button.short_description = 'Загрузка XML'
    upload_xml_button.allow_tags = True

    change_list_template = 'admin/property_finder_change_list.html'


@admin.register(Region, Home, PopularPlaces, ToTry, Culture,
                Games, NationalClothes, HandCrafts, NationalInstruments)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class CultureKitchenImageInline(admin.TabularInline):
    model = CultureKitchenImage
    extra = 1


@admin.register(CultureKitchen)
class CultureKitchenAdmin(TranslationAdmin):
    inlines = [CultureKitchenImageInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class AttractionsImageInline(admin.TabularInline):
    model = AttractionsImage
    extra = 1


@admin.register(Attractions)
class AttractionsAdmin(TranslationAdmin):
    inlines = [AttractionsImageInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class HotelsImageInlines(admin.TabularInline):
    model = HotelsImage
    extra = 1


class AmenitiesInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = Amenities
    extra = 1


class SafetyAndHygieneInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = SafetyAndHygiene
    extra = 1


@admin.register(Hotels)
class HotelsAdmin(TranslationAdmin):
    inlines = [HotelsImageInlines, AmenitiesInline, SafetyAndHygieneInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class KitchenLocationInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = KitchenLocation
    extra = 1


class KitchenImageInline(admin.TabularInline):
    model = KitchenImage
    extra = 1


@admin.register(Kitchen)
class KitchenAdmin(TranslationAdmin):
    inlines = [KitchenImageInline, KitchenLocationInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(EventCategories)
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(CultureCategory)
admin.site.register(Region_Categoty)
admin.site.register(Ticket)
admin.site.unregister(Group)


class Currency_DescriptionInlines(TranslationInlineModelAdmin, admin.TabularInline):
    model = Currency_Description
    extra = 1


class Currency_ImageInlines(admin.TabularInline):
    model = Currency_Image
    extra = 1


@admin.register(Currency)
class CultureKitchenAdmin(TranslationAdmin):
    inlines = [Currency_DescriptionInlines, Currency_ImageInlines]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CultureKitchenMain)
class CultureKitchenMainAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class AirLineDirectionsInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = AirLineDirections
    extra = 1


@admin.register(AirLineTickets)
class AirLineTicketsAdmin(TranslationAdmin):
    inlines = [AirLineDirectionsInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(KitchenReview)