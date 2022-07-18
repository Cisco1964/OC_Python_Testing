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

    places = [
        {
            "competition": "Competition",
            "booked": [8, "Club"]
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club
        server.places = self.places

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
        assert "Vous ne pouvez pas reserver plus de 12 places" in rv.data.decode()
        assert rv.status_code == 400

    def test_more_12_add(self):
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
        #assert "Vous ne pouvez pas reserver plus de 12 places" in rv.data.decode()
        assert "Pas assez de place disponible" in rv.data.decode()