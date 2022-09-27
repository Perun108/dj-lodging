import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED

from djlodging.domain.lodgings.models.review import Review
from tests.domain.lodgings.factories import LodgingFactory

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

    # def test_create_lodging_by_non_partner_fails(self, user_api_client_pytest_fixture):
    #     city = CityFactory()

    #     name = fake.word()
    #     type = random.choice(Lodging.Type.choices)
    #     street = fake.street_name()
    #     house_number = fake.building_number()
    #     zip_code = fake.postcode()
    #     email = fake.email()
    #     phone_number = fake.phone_number()

    #     payload = {
    #         "name": name,
    #         "type": type,
    #         "city_id": str(city.id),
    #         "street": street,
    #         "house_number": house_number,
    #         "zip_code": zip_code,
    #         "email": email,
    #         "phone_number": phone_number,
    #         "price": 10,
    #     }

    #     url = reverse("lodging-list")  # POST "/api/lodgings/"

    #     response = user_api_client_pytest_fixture.post(url, payload)

    #     assert response.status_code == HTTP_403_FORBIDDEN
