#!/usr/bin/python
# -*- coding: utf-8 -*-
import server
from server import app



class Testintegration:
    client = app.test_client()
   
    server.competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    server.clubs =  [
        {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        }
    ]


    def test_index(self):
        # rv = self.client.get('/')
        # assert rv.status_code == 200
        
        rv = self.client.get('/')
        assert rv.status_code == 200
        assert b'email' in rv.data


    def test_email(self):
        result = self.client.post("/showSummary", data={"email": server.clubs[0]["email"]})
        assert result.status_code == 200
        assert f"{server.clubs[0]['email']}" in result.data.decode()


    def test_one_point(self):
        rv = self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": server.clubs[0]["name"],
                "competition": server.competitions[0]["name"]
            }
        )

        assert rv.status_code == 200
        assert "Great-booking complete!" in rv.data.decode()
        assert int(server.clubs[0]["points"]) >= 0


    def test_points(self):
        club_points = int(server.clubs[0]["points"])
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
        assert int(server.clubs[0]["points"]) == club_points - (placesRequired * 3)

        rv = self.client.get('/clubpoints')

        assert f"<td>{server.clubs[0]['name']}</td>" in rv.data.decode()
        assert f"<td>{club_points - placesRequired * 3}</td>" in rv.data.decode()
        

    def test_logout(self):
         rv = self.client.get('/logout')
         assert rv.status_code == 302
