import server
from server import app


class TestPointUpdate:
    client = app.test_client()
   
    server.competitions = [
        {
            "name": "Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    server.clubs =  [
        {
            "name": "Club",
            "email": "toto@gmail.com",
            "points": "13"
        }
    ]

    def test_points(self):
        club_points = int(server.clubs[0]["points"])
        placesRequired = 4
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
        assert int(server.clubs[0]["points"]) == club_points - placesRequired 

    def test_equal_blank(self):
        placesRequired = ""
        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": placesRequired,
                "club": server.clubs[0]["name"],
                "competition": server.competitions[0]["name"]
            }
        )
        assert rv.status_code == 400
        assert "Saisir un nombre entre 0 et 12, Veuillez recommencer" in rv.data.decode()
