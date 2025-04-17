from rest_framework import generics, status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework.templatetags.rest_framework import data
from django_rest_passwordreset.views import ResetPasswordRequestToken
from rest_framework.decorators import api_view
from .serializers import UserSerializer, LoginSerializer, EmptySerializer, VerifyResetCodeSerializer
from country.serializers import AttractionReviewSimpleSerializer, PopularReviewSimpleSerializer, \
    HotelsReviewSimpleSerializer, KitchenReviewSimpleSerializer
from country.models import  AttractionReview, PopularReview, HotelsReview, KitchenReview
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ValidationError as SerializerValidationError


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            # Проверяем валидность данных и сразу получаем ошибки, если они есть
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except SerializerValidationError as e:
            # Обрабатываем ошибки валидации от сериализатора
            error_detail = e.detail
            error_message = ""
            if isinstance(error_detail, dict):
                # Извлекаем первое сообщение об ошибке
                for field, errors in error_detail.items():
                    if isinstance(errors, list) and errors:
                        error_message = str(errors[0])
                        break
                    else:
                        error_message = str(errors)
                        break
            else:
                error_message = str(error_detail)

            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Обрабатываем остальные ошибки как серверные
            return Response(
                {"detail": f"Сервер не работает, {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'detail': f'Поле {field} обязательно'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            response_data = {
                'access': str(access),
                'refresh': str(refresh),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            # Проверяем сообщение об ошибке и возвращаем нужный ответ
            error_detail = e.detail[0] if isinstance(e.detail, list) else e.detail
            if error_detail == 'Пользователь не найден':
                return Response(
                    {'detail': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            elif error_detail == 'Неверный пароль':
                return Response(
                    {'detail': 'Неверный пароль'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            elif error_detail == 'Пользователь неактивен':
                return Response(
                    {'detail': 'Пользователь неактивен'},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                return Response(
                    {'detail': 'Неверные учетные данные'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {"detail": f"Сервер не работает, {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        try:
            access_token = request.COOKIES.get('access_token')
            if not access_token:
                return Response({'error': 'Access токен отсутствует'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = AccessToken(access_token)
                token.blacklist()
            except (TokenError, AttributeError):
                pass

            response = Response({'message': 'Вы успешно вышли'}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserCommentsHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            attraction = AttractionReview.objects.filter(client=user)
            popular_review = PopularReview.objects.filter(client=user)
            hotel_review = HotelsReview.objects.filter(client=user)
            kitchen_review = KitchenReview.objects.filter(client=user)

            serialized_attraction_review = AttractionReviewSimpleSerializer(attraction, many=True).data
            serialized_popular_review = PopularReviewSimpleSerializer(popular_review, many=True).data
            serialized_hotel_review = HotelsReviewSimpleSerializer(hotel_review, many=True).data
            serialized_kitchen_review = KitchenReviewSimpleSerializer(kitchen_review, many=True).data

            combined_reviews = list(chain(serialized_attraction_review, serialized_popular_review,
                                          serialized_hotel_review, serialized_kitchen_review))
            return Response(combined_reviews)
        except IntegrityError as e:
            return Response(
                {"error": "There was an issue retrieving user comments.", "details": str(e)},
                status=500
            )


@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def custom_password_reset(request):
    response = ResetPasswordRequestToken.as_view()(request._request)
    if response.status_code == 200:
        return Response({'status': "Код отправлен"}, status=status.HTTP_200_OK)
    return response