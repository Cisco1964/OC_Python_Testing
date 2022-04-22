import server
from server import app


class TestMore12Points:
    client = app.test_client()
    competition = [
        {
            "name": "Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "40"
        }
    ]

    club = [
        {
            "name": "Club",
            "email": "toto@gmail.com",
            "points": "20"
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

    def test_more_12_once(self):
        placesRequired = 13

        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": placesRequired,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )
        assert "Pas assez de place disponible" in rv.data.decode()
        assert rv.status_code == 400

    def test_more_12_added(self):
        placesRequired = 10

        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": placesRequired,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )
        assert rv.status_code == 400
        assert "Pas assez de place disponible" in rv.data.decode()