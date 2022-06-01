import server
from server import app


class TestMorePoints:
    client = app.test_client()
    competition = [
        {
            "name": "Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Club",
            "email": "toto@gmail.com",
            "points": "13"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_points(self):
        placesRequired = 1 
        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": placesRequired,
                "club": server.clubs[0]["name"],
                "competition": server.competitions[0]["name"]
            }
        )
        assert rv.status_code == 200
        assert "Great-booking complete!" in rv.data.decode()


    def test_add_points(self):
        placesRequired = 5 
        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": placesRequired,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert rv.status_code == 400
        assert "Vous ne pouvez pas reserver plus de 12 places" in rv.data.decode()
        assert int(self.club[0]["points"]) >= 0

    def test_more_points(self):
        placesRequired = 14 
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
        