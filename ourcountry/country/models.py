from multiselectfield import MultiSelectField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from accounts.models import UserProfile
from solo.models import SingletonModel


class PropertyFinder(SingletonModel):
    file = models.FileField(verbose_name='Файл')

    class Meta:
        verbose_name = 'Property Finder'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file.name


class Region_Categoty(models.Model):
    CHOICES = (
        ('Chui', 'Chui'),
        ('Talas', 'Talas'),
        ('Batken', 'Batken'),
        ('Osh', 'Osh'),
        ('Naryn', 'Naryn'),
        ('Issyk-Kul', 'Issyk-Kul'),
        ('Jalal-Abad', 'Jalal-Abad'),
    )
    region_category = models.CharField('Категории Регионов', max_length=20, choices=CHOICES)

    def __str__(self):
        return self.region_category

    class Meta:
        verbose_name = 'Категории Регионов'
        verbose_name_plural = 'Категории Регионов'


class Region(models.Model):
    region_name = models.CharField('Названия Региона', max_length=55)
    region_image = models.FileField('Фото', upload_to='region_images')
    region_description = models.TextField('Описание')
    region_category = models.ForeignKey(
        Region_Categoty,
        on_delete=models.CASCADE,
        related_name='region',
        verbose_name='Категории Регионов',
    )
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта')

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Регионы'
        verbose_name_plural = 'Регионы'


class Home(models.Model):
    home_name = models.CharField('Заголовок', max_length=55)
    home_image = models.FileField('Фото', upload_to='home_images', null=True, blank=True)
    home_description = models.TextField('Описание')

    def __str__(self):
        return self.home_name

    class Meta:
        verbose_name = 'Главная Страница'
        verbose_name_plural = 'Главная Страница'


class PopularPlaces(models.Model):
    popular_name = models.CharField('Название', max_length=250)
    popular_image = models.FileField('Фото', upload_to='popular_images')
    description = models.TextField('Фото')
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='popular_places',
        verbose_name='Регион'
    )
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта')
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.popular_name}'

    class Meta:
        verbose_name = 'Популярные места'
        verbose_name_plural = 'Популярные места'

    def get_avg_rating(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def get_excellent(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_attraction_len(self):
        len = self.popular_places.all()
        if len.exists():
            return len.count()
        return 0


class Attractions(models.Model):
    attraction_name = models.CharField('Название', max_length=155)
    description = models.TextField('Описание')
    region_category = models.ForeignKey(
        Region_Categoty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Регион"
    )
    popular_places = models.ForeignKey(
        PopularPlaces,
        on_delete=models.CASCADE,
        related_name='popular_places',
        null=True,
        blank=True,
        verbose_name="Популярные места"
    )
    main_image = models.FileField('Фото на Главный Фон', upload_to='main_image/', null=True, blank=True)
    type_attraction = models.CharField("Тип Достопримечательности", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.attraction_name

    class Meta:
        verbose_name = 'Достопримечательности'
        verbose_name_plural = 'Достопримечательности'

    def get_excellent(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_avg_rating(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            return ratings.count()
        return 0

    @staticmethod
    def get_attractions_by_excellent():
        attractions = Attractions.objects.all()
        sorted_attractions = sorted(attractions, key=lambda attraction: attraction.get_excellent(), reverse=True)
        for index, attraction in enumerate(sorted_attractions):
            attraction.rank = index + 1
        return sorted_attractions

    def get_rank(self):
        sorted_attractions = Attractions.get_attractions_by_excellent()
        for index, attraction in enumerate(sorted_attractions):
            if attraction == self:
                return index + 1
        return None


class AttractionsImage(models.Model):
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name='image')
    image = models.FileField('Фото', upload_to='attartions_image/', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото Для Достопримечательности'
        verbose_name_plural = 'Фото Для Достопримечательности'


class AttractionReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='home_reviews')
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name='attractions_review')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True, verbose_name='Рейтинг')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}'


class ReplyToAttractionReview(models.Model):
    review = models.ForeignKey(AttractionReview, on_delete=models.CASCADE, related_name='reply_attraction_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client')
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class AttractionsReviewImage(models.Model):
    attractions = models.ForeignKey(AttractionReview, on_delete=models.CASCADE, related_name='attraction_review_image')
    image = models.FileField(upload_to='attraction_review_image/', null=True, blank=True)


class PopularReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    popular_place = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, related_name='popular_reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True, verbose_name='Рейтинг')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}-{self.popular_place}'



class ReplyToPopularReview(models.Model):
    review = models.ForeignKey(PopularReview, on_delete=models.CASCADE, related_name='reply_popular_places')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class ReviewImage(models.Model):
    review = models.ForeignKey(PopularReview, on_delete=models.CASCADE, related_name='review_image')
    image = models.FileField(upload_to='review_images/', null=True, blank=True)


class ToTry(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='What_to_try', verbose_name="Регион")
    to_name = models.CharField('Названия блюда', max_length=200)
    first_description = models.TextField('Первое Описание')
    second_description = models.TextField('Второе Описание')
    image = models.FileField('Фото', upload_to='to_try_image/', null=True, blank=True)

    def __str__(self):
        return self.to_name

    class Meta:
        verbose_name = 'Eда регионов'
        verbose_name_plural = 'Eда регионов'


class Hotels(models.Model):
    name = models.CharField('Название Гостиницы', max_length=155)
    description = models.TextField('Описание')
    main_image = models.FileField('Главное Фото', upload_to='main_image/', null=True, blank=True)
    region = models.ForeignKey(
        Region_Categoty,
        on_delete=models.CASCADE,
        related_name='hotels_region',
        null=True,
        blank=True,
        verbose_name="Регион"
    )
    popular_places = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, verbose_name="Популярная места")
    address = models.CharField('Адрес', max_length=100)
    bedroom = models.PositiveIntegerField('Спальная комната', default=1)
    bathroom = models.PositiveIntegerField('Ванная комната', default=1)
    cars = models.PositiveIntegerField('Машины', default=1)
    bikes = models.PositiveIntegerField('Велосипеды', default=1)
    pets = models.PositiveIntegerField('Домашние Животные')
    price_short_period = models.PositiveIntegerField('Цена Короткого Периода')
    price_medium_period = models.PositiveIntegerField('Цена Среднего Периода')
    price_long_period = models.PositiveIntegerField('Цена Долгого Периода')
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта')
    contact = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Контактный номер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гостиницы'
        verbose_name_plural = 'Гостиницы'

    def get_excellent(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_avg_rating(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0


class Amenities(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name="amenities")
    amenity = models.CharField('Называние Удобства', max_length=55)
    icon = models.FileField('Иконка', upload_to='icons/')

    class Meta:
        verbose_name = 'Удобства'
        verbose_name_plural = 'Удобства'


class SafetyAndHygiene(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='safety_and_hygiene')
    name = models.CharField('Название', max_length=55)

    class Meta:
        verbose_name = 'Безопасность и Гигиена'
        verbose_name_plural = 'Безопасность и Гигиена'


class HotelsImage(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='hotel_image')
    image = models.FileField('Фото', upload_to='hotel_images/', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото Гостиницы'
        verbose_name_plural = 'Фото Гостиницы'


class HotelsReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_hotel')
    comment = models.TextField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='hotel_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.client}'


class ReplyToHotelReview(models.Model):
    review = models.ForeignKey(HotelsReview, on_delete=models.CASCADE, related_name='reply_hotel_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class HotelsReviewImage(models.Model):
    hotel_review = models.ForeignKey(HotelsReview, on_delete=models.CASCADE, related_name='hotel_review_image')
    image = models.FileField(upload_to='hotel_review_image/', null=True, blank=True)


class Kitchen(models.Model):
    kitchen_name = models.CharField('Название Кафе', max_length=155)
    description = models.TextField("Описание")
    main_image = models.FileField('Фото на Главный Фон', upload_to='main_image/', null=True, blank=True)
    kitchen_region = models.ForeignKey(
        Region_Categoty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Регион'
    )
    popular_places = models.ForeignKey(
        PopularPlaces,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Популярная Места'
    )
    price = models.PositiveIntegerField('Цена')
    specialized_menu = models.TextField('Специализированное Меню', default="Подходит для вегетарианцев, Для веганов")
    MEAL_TIME = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Brunch', 'Brunch'),
        ('Open Late', 'Open Late'),
        ('Drinks', 'Drinks'),
    )
    meal_time = MultiSelectField('Время Еды', choices=MEAL_TIME)
    TYPE = (
        ('Russian', 'Russian'),
        ('Asian', 'Asian'),
        ('Canadian', 'Canadian'),
        ('Chinese', 'Chinese'),
        ('European', 'European'),
        ('Japan', 'Japan'),
        ('Korean', 'Korean'),
    )
    type_of_cafe = MultiSelectField('Тип кафе', choices=TYPE)

    def __str__(self):
        return self.kitchen_name

    class Meta:
        verbose_name = 'Kaфе'
        verbose_name_plural = 'Kaфе'

    def get_average_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.rating for rating in ratings if rating.rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_rating_count(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def get_nutrition_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.nutrition_rating for rating in ratings if rating.nutrition_rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_service_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.service_rating for rating in ratings if rating.service_rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_price_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.price_rating for rating in ratings if rating.price_rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_atmosphere_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.atmosphere_rating for rating in ratings if rating.atmosphere_rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_excellent(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    @staticmethod
    def get_attractions_by_excellent():
        attractions = Kitchen.objects.all()
        sorted_attractions = sorted(attractions, key=lambda attraction: attraction.get_excellent(), reverse=True)
        for index, attraction in enumerate(sorted_attractions):
            attraction.rank = index + 1
        return sorted_attractions

    def get_rank(self):
        sorted_attractions = Kitchen.get_attractions_by_excellent()
        for index, attraction in enumerate(sorted_attractions):
            if attraction == self:
                return index + 1
        return None


class KitchenLocation(models.Model):
    address = models.TextField('Адрес')
    website = models.URLField('Ссылкана сайт', null=True, blank=True)
    email = models.CharField(max_length=60)
    phone_number = PhoneNumberField('Телефон номер', null=True, blank=True, region='KG')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen')
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта')

    class Meta:
        verbose_name = 'Локация Кафе'
        verbose_name_plural = 'Локация Кафе'


class KitchenImage(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_image')
    image = models.FileField('Фото', upload_to='kitchen_images/', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото Кафе'
        verbose_name_plural = 'Фото Кафе'


class KitchenReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    nutrition_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    service_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    price_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    atmosphere_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}'


class ReplyToKitchenReview(models.Model):
    review = models.ForeignKey(KitchenReview, on_delete=models.CASCADE, related_name='reply_kitchen_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class KitchenReviewImage(models.Model):
    review = models.ForeignKey(KitchenReview, on_delete=models.CASCADE, related_name='kitchen_review_image')
    image = models.FileField(upload_to='kitchen_review_image/', null=True, blank=True)


class EventCategories(models.Model):
    CATEGORIES = (
        ('Concert', 'Concert'),
        ('Cinema', 'Cinema'),
        ('Leisure', 'Leisure'),
        ('Exhibitions', 'Exhibitions'),
        ('Theater', 'Theater'),
        ('Master classes', 'Master classes'),
        ('Tourism', 'Tourism'),
    )
    category = models.CharField('Категория', max_length=20, choices=CATEGORIES, null=True, blank=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категории мероприятий'
        verbose_name_plural = 'Категории мероприятий'


class Event(models.Model):
    category = models.ForeignKey(
        EventCategories,
        on_delete=models.CASCADE,
        related_name='event_category',
        verbose_name='Категория'
    )
    image = models.FileField('Фото', upload_to='event_images/', null=True, blank=True)
    popular_places = models.ForeignKey(
        PopularPlaces,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Популярная Места"
    )
    title = models.CharField('Название', max_length=52)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    address = models.CharField('Адрес', max_length=150)
    price = models.PositiveIntegerField('Цена')
    ticket = models.BooleanField('Билеты', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мероприятия'
        verbose_name_plural = 'Мероприятия'


class Ticket(models.Model):
    concert = models.ForeignKey(
        EventCategories,
        on_delete=models.CASCADE,
        related_name='concert',
        verbose_name='Категория'
    )
    image = models.FileField('Фото', upload_to='event_images/', null=True, blank=True)
    title = models.CharField('Название', max_length=52)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    address = models.CharField('Адрес', max_length=150)
    price = models.PositiveIntegerField('Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Билеты Мероприятий'
        verbose_name_plural = 'Билеты Мероприятий'


class CultureCategory(models.Model):
    CATEGORIES = (
        ("Games", "Games"),
        ("National clothes", "National clothes"),
        ("Hand crafts", "Hand crafts"),
        ("Currency", "Currency"),
        ("National instruments", "National instruments"),
        ("Kitchen", "Kitchen"),
    )
    culture_name = models.CharField('Категория', max_length=35, choices=CATEGORIES)

    def __str__(self):
        return self.culture_name

    class Meta:
        verbose_name = 'Категория Культура'
        verbose_name_plural = 'Категория Культура'


class Culture(models.Model):
    culture_name = models.CharField('Название', max_length=35)
    culture_description = models.TextField('Описание')
    culture_image = models.FileField('Фото', upload_to='culture-images')
    culture = models.ForeignKey(
        CultureCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Категория"
    )

    def __str__(self):
        return self.culture_name

    class Meta:
        verbose_name = 'Культура'
        verbose_name_plural = 'Культура'


class Games(models.Model):
    games_name = models.CharField('Название', max_length=300)
    games_description = models.TextField("Описание")
    games_image = models.FileField("Фото", upload_to='games_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.games_name

    class Meta:
        verbose_name = 'Национальные Игры'
        verbose_name_plural = 'Национальные Игры'


class NationalClothes(models.Model):
    clothes_name = models.CharField('Название', max_length=300)
    clothes_description = models.TextField("Описание")
    clothes_image = models.FileField("Фото", upload_to='clothes_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.clothes_name

    class Meta:
        verbose_name = 'Национальные Одежды'
        verbose_name_plural = 'Национальные Одежды'


class HandCrafts(models.Model):
    hand_name = models.CharField('Название', max_length=300)
    hand_description = models.TextField('Описание')
    hand_image = models.FileField('Фото', upload_to='hand_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.hand_name

    class Meta:
        verbose_name = 'Рукоделие'
        verbose_name_plural = 'Рукоделие'


class Currency(models.Model):
    currency_name = models.CharField('Название', max_length=300)
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.currency_name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюта'


class Currency_Description(models.Model):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='currency_description',
        null=True,
        blank=True,
        verbose_name='Валюта'
    )
    description = models.TextField('Описание')


class Currency_Image(models.Model):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='currency_image',
        null=True,
        blank=True,
        verbose_name='Валюта'
    )
    front_image = models.FileField('Переднее изображение', upload_to='front_image_currency', null=True, blank=True)
    back_image = models.FileField('Заднее изображение', upload_to='back_image_currency', null=True, blank=True)


class NationalInstruments(models.Model):
    national_name = models.CharField('Название', max_length=300)
    national_description = models.TextField('Описание')
    national_image = models.FileField('Фото', upload_to='national_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.national_name

    class Meta:
        verbose_name = 'Национальные Инструменты'
        verbose_name_plural = 'Национальные Инструменты'


class CultureKitchen(models.Model):
    kitchen_name = models.CharField('Название', max_length=300)
    kitchen_description = models.TextField('Описание')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.kitchen_name

    class Meta:
        verbose_name = 'Национальные Блюда'
        verbose_name_plural = 'Национальные Блюда'


class CultureKitchenImage(models.Model):
    culture_kitchen = models.ForeignKey(
        CultureKitchen,
        on_delete=models.CASCADE,
        related_name='culture_kitchen_image',
        verbose_name='Национальное Блюдо'
    )
    image = models.FileField('Фото', upload_to='culture_kitchen_image/', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото Национальных Блюд'
        verbose_name_plural = 'Фото Национальных Блюд'


class CultureKitchenMain(models.Model):
    title = models.CharField('Название', max_length=100)
    description = RichTextField('Описание')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, verbose_name='Категория')
    image_1 = models.FileField('Изображение 1', upload_to='culture_kitchen_image', null=True, blank=True)
    image_2 = models.FileField('Изображение 2', upload_to='culture_kitchen_image', null=True, blank=True)
    image_3 = models.FileField('Изображение 3', upload_to='culture_kitchen_image', null=True, blank=True)
    image_4 = models.FileField('Изображение 4', upload_to='culture_kitchen_image', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Национальные Блюда'
        verbose_name_plural = 'Национальные Блюда'


class AirLineTickets(models.Model):
    logo = models.FileField('Логотип', upload_to='airline_logos/', null=True, blank=True)
    name = models.CharField('Название', max_length=250)
    description = models.TextField('Описание')
    website = models.URLField('Вебсайт')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Авиа Билеты'
        verbose_name_plural = 'Авиа Билеты'


class AirLineDirections(models.Model):
    ticket = models.ForeignKey(
        AirLineTickets,
        on_delete=models.CASCADE,
        related_name='airline_tickets',
        verbose_name='Авиабилет'
    )
    directions = models.CharField('Направление', max_length=250)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направление'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, null=True, blank=True)
    popular_place = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=True, blank=True)
    hotels = models.ForeignKey(Hotels, on_delete=models.CASCADE, null=True, blank=True)
    like = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.attractions:
            existing = Favorite.objects.filter(
                user=self.user,
                attractions=self.attractions,
                popular_place__isnull=True,
                kitchen__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        elif self.popular_place:
            existing = Favorite.objects.filter(
                user=self.user,
                popular_place=self.popular_place,
                attractions__isnull=True,
                kitchen__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        elif self.kitchen:
            existing = Favorite.objects.filter(
                user=self.user,
                kitchen=self.kitchen,
                attractions__isnull=True,
                popular_place__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        elif self.hotels:
            existing = Favorite.objects.filter(
                user=self.user,
                hotels=self.hotels,
                attractions__isnull=True,
                popular_place__isnull=True,
                kitchen__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        return super().save(*args, **kwargs)