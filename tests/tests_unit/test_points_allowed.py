import server
from server import app


class TestMoreThanTwelvePoints:
    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2020-04-22 10:30:00",
            "numberOfPlaces": "20"
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "test@email.com",
            "points": "12"
        }
    ]

    places_booked = [
        {
            "competition": "Test",
            "booked": [5, "Test club"]
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club
        server.places_booked = self.places_booked

    def test_less_than_twelve(self):
        booked = 5

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        #assert result.status_code == 200
        assert "Great-booking complete!" in result.data.decode()
        assert int(self.club[0]["points"]) >= 0

    def test_more_than_twelve_added(self):
        booked = 13

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 400
        assert "Pas assez de place disponible" in result.data.decode()  
        assert int(self.club[0]["points"]) >= 0
       