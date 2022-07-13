#!/usr/bin/python
# -*- coding: utf-8 -*-
from turtle import delay
from locust import HttpUser, task, between

class ProjectPerfTest(HttpUser):
    wait_time = between(5, 20)
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2022-09-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    club =  [
        {
            "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        }
    ]

    def on_start(self):
        self.client.get('/')
        response = self.client.post('/showSummary', {'email': self.club[0]["email"]}, 
            name="/showSummary")
        

    def on_stop(self):
        self.client.get('/logout')


    @task
    def booking(self):
        #with self.client.get("/book/Spring Festival/She Lifts", catch_response=True) as response:
        rv = f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        rv = rv.replace('%20', ' ')
        self.client.get(rv) 


    # @task(1)
    @task
    def purchase(self): 
        # self.client.post("/purchasePlaces", 
        #             data={"places": 1, 
        #             "club": self.club[0]['name'], 
        #             "competition": self.competitions[0]['name']}) 

        self.client.post(
            "/purchasePlaces",
            data={
                "places": 0,
                "club": self.club[0]["name"],
                "competition": self.competitions[0]["name"]
            }
        )

    @task
    def clubpoint(self):
        self.client.get("/clubpoints")
    

        # with self.client.post("/purchasePlaces", data={"places": 1, 
        #           "club": self.club[0]['name'], 
        #            "competition": self.competitions[0]['name']}, catch_response=True) as response:
        #     if response.status_code != 200:
        #         response.failure("Erreur inattendue : " + str(response.status_code) + " Erreur: " + str(response.text))
        #     else:
        #         print("/purchasePlaces : Test OK")
        # response.success() 

#class WebsiteUser(HttpUser):
    #task_set = ProjectPerfTest
    #wait_time = between(5, 20)
