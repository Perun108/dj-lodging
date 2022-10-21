import pytest
from faker import Faker
from pytest_django.asserts import assertQuerysetEqual
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from djlodging.domain.lodgings.models.review import Review
from tests.domain.lodgings.factories import LodgingFactory, ReviewFactory
from tests.domain.users.factories import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestReviewViewSet:
    def test_list_reviews_succeeds(self, user_api_client_pytest_fixture):
        tested_lodging = LodgingFactory()
        tested_lodging_reviews_count = 5
        another_lodging = LodgingFactory()
        another_lodging_reviews_count = 3

        # Create tested reviews
        ReviewFactory.create_batch(size=tested_lodging_reviews_count, lodging=tested_lodging)
        # Create other (not tested) reviews
        ReviewFactory.create_batch(size=another_lodging_reviews_count, lodging=another_lodging)

        total_reviews_count = Review.objects.count()
        assert total_reviews_count == tested_lodging_reviews_count + another_lodging_reviews_count

        url = reverse(
            "reviews-list", args=[str(tested_lodging.id)]
        )  # GET "/api/lodgings/{lodging_id}/reviews/"

        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == tested_lodging_reviews_count

    def test_list_without_reviews_succeeds(self, user_api_client_pytest_fixture):
        tested_lodging = LodgingFactory()

        url = reverse(
            "reviews-list", args=[str(tested_lodging.id)]
        )  # GET "/api/lodgings/{lodging_id}/reviews/"

        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_succeeds(self, user_api_client_pytest_fixture):
        lodging = LodgingFactory()
        review = ReviewFactory(lodging=lodging)
        review_id = str(review.id)

        url = reverse(
            "reviews-detail", args=[str(lodging.id), review_id]
        )  # GET "/api/lodgings/{lodging_id}/reviews/{review_id}/"

        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == review_id


@pytest.mark.django_db
class TestMyReviewViewSet:
    def test_create_review_succeeds(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        text = fake.paragraph()
        score = int(fake.numerify("#"))

        payload = {"lodging_id": lodging.id, "text": text, "score": score}

        url = reverse("my-reviews-list")  # POST "/api/users/me/reviews/"

        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        review = Review.objects.first()
        assert review.lodging == lodging
        assert review.user == user
        assert review.text == text
        assert review.score == score

    def test_list_my_reviews_for_multiple_lodgings_succeeds(
        self, user_api_client_pytest_fixture, user
    ):
        lodging_1 = LodgingFactory()
        lodging_1_reviews_number = 3
        lodging_1_reviews = ReviewFactory.create_batch(
            size=lodging_1_reviews_number, lodging=lodging_1, user=user
        )

        lodging_2 = LodgingFactory()
        lodging_2_reviews_number = 2
        lodging_2_reviews = ReviewFactory.create_batch(
            size=lodging_2_reviews_number, lodging=lodging_2, user=user
        )

        url = reverse("my-reviews-list")  # GET "/api/users/me/reviews/"
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == lodging_1_reviews_number + lodging_2_reviews_number
        assertQuerysetEqual(
            Review.objects.all(), lodging_1_reviews + lodging_2_reviews, ordered=False
        )

    def test_list_my_reviews_for_multiple_lodgings_with_other_users_reviews_succeeds(
        self, user_api_client_pytest_fixture, user
    ):
        lodging_1 = LodgingFactory()
        lodging_1_reviews_number = 3
        ReviewFactory.create_batch(size=lodging_1_reviews_number, lodging=lodging_1, user=user)

        lodging_2 = LodgingFactory()
        lodging_2_reviews_number = 2
        ReviewFactory.create_batch(size=lodging_2_reviews_number, lodging=lodging_2, user=user)

        another_user = UserFactory()
        another_user_reviews_number = 3
        ReviewFactory.create_batch(
            size=another_user_reviews_number, user=another_user, lodging=lodging_1
        )

        url = reverse("my-reviews-list")  # GET "/api/users/me/reviews/"
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert (
            Review.objects.count()
            == lodging_1_reviews_number + lodging_2_reviews_number + another_user_reviews_number
        )
        assert len(response.data) == lodging_1_reviews_number + lodging_2_reviews_number

    def test_list_without_my_reviews_succeeds(self, user_api_client_pytest_fixture, user):
        another_user = UserFactory()
        ReviewFactory(user=another_user)

        assert Review.objects.count() == 1

        url = reverse("my-reviews-list")
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0

    def test_retrieve_my_succeeds(self, user_api_client_pytest_fixture, user):
        review = ReviewFactory(user=user)
        review_id = str(review.id)

        url = reverse(
            "my-reviews-detail", args=[review_id]
        )  # GET "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == review_id

    def test_retrieve_my_by_another_user_fails(self, user_api_client_pytest_fixture, user):
        me = UserFactory()
        review = ReviewFactory(user=me)
        review_id = str(review.id)

        url = reverse(
            "my-reviews-detail", args=[review_id]
        )  # GET "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.get(url)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_update_my_succeeds(self, user_api_client_pytest_fixture, user):
        review = ReviewFactory(user=user)

        new_text = fake.paragraph()
        new_score = int(fake.numerify("#"))

        review_id = str(review.id)

        payload = {"text": new_text, "score": new_score}
        url = reverse(
            "my-reviews-detail", args=[review_id]
        )  # GET "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.put(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == review_id
        assert response.data["text"] == new_text
        assert response.data["score"] == new_score

    def test_update_my_by_another_user_fails(self, user_api_client_pytest_fixture, user):
        me = UserFactory()
        review = ReviewFactory(user=me)
        review_id = str(review.id)

        new_text = fake.paragraph()
        new_score = int(fake.numerify("#"))

        payload = {"text": new_text, "score": new_score}
        url = reverse(
            "my-reviews-detail", args=[review_id]
        )  # GET "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.put(url, payload)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_my_succeeds(self, user_api_client_pytest_fixture, user):
        review = ReviewFactory(user=user)
        assert Review.objects.first() == review

        url = reverse(
            "my-reviews-detail", args=[str(review.id)]
        )  # DELETE "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert Review.objects.first() is None

    def test_delete_my_by_another_user_fails(self, user_api_client_pytest_fixture, user):
        me = UserFactory()
        review = ReviewFactory(user=me)
        review_id = str(review.id)

        url = reverse(
            "my-reviews-detail", args=[review_id]
        )  # DELETE "/api/users/me/reviews/{review_id}/"
        response = user_api_client_pytest_fixture.delete(url)

        assert response.status_code == HTTP_403_FORBIDDEN
        assert Review.objects.first() == review
