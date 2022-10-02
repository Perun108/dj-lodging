import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from djlodging.domain.lodgings.models.review import Review
from tests.domain.lodgings.factories import LodgingFactory, ReviewFactory

fake = Faker()


@pytest.mark.django_db
class TestReviewViewSet:
    def test_create_review_succeeds(self, user_api_client_pytest_fixture, user):
        lodging = LodgingFactory()
        text = fake.paragraph()
        score = int(fake.numerify("#"))

        payload = {"text": text, "score": score}

        url = reverse(
            "reviews-list", args=[str(lodging.id)]
        )  # POST "/api/lodgings/{lodging_id}/reviews/"

        response = user_api_client_pytest_fixture.post(url, payload)

        assert response.status_code == HTTP_201_CREATED

        review = Review.objects.first()
        assert review.lodging == lodging
        assert review.user == user
        assert review.text == text
        assert review.score == score

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
