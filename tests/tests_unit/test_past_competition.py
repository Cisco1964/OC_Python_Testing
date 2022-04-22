import server
from server import app


class TestPastCompetition:
    client = app.test_client()

    competitions = [
        {
            "name": "Competition",
            "date": "2022-04-01 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    club =  [
        {
            "name": "Club",
            "email": "toto@gmail.com",
            "points": "13"
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.club

    def test_book_competitions(self):
        # /book/<competition>/<club>
        rv = self.client.get(
            f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        )
        
        assert "Cette competition est déjà terminée." in rv.data.decode()
        assert rv.status_code == 400
        