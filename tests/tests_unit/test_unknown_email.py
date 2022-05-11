import server
from server import app


class TestUnknownEmail:
    client = app.test_client()

    club = [
        {
            "name": "Club",
            "email": "toto@gmail.com",
            "points": "13"
        }
    ]

    def setup_method(self):
        server.clubs = self.club

    def test_valid_email(self):
        result = self.client.post("/showSummary", data={"email": server.clubs[0]["email"]})
        assert result.status_code == 200
        assert f"{server.clubs[0]['email']}" in result.data.decode()

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data={"email": "toto"})
        assert result.status_code == 401
        assert "Email inconnu" in result.data.decode()

    def test_empty_email(self):
        result = self.client.post("/showSummary", data={"email": ""})
        assert result.status_code == 401
        assert "Veuillez saisir votre adresse mail" in result.data.decode()