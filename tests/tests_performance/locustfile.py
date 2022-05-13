#!/usr/bin/python
# -*- coding: utf-8 -*-
from turtle import delay
from locust import HttpUser, task, between

class ProjectPerfTest(HttpUser):
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
        print("RESPONSE", response.status_code)
        

    def on_stop(self):
        self.client.get('/logout')


    @task(1)
    def booking(self):
        #s = f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
        #s = s.replace('%20',' ')
        #rv = self.client.get(
        #        s, 
        #        name="book"
        #)
        rv = "/book/Spring Festival/She Lifts"
        rv = rv.replace('%20', ' ')
        #self.client.get(rv, name=rv)
        
        #print("RV", rv.status_code)
        #print("type RV", type(rv))
        with self.client.get("/book/Spring Festival/She Lifts", catch_response=True) as response:
            if response.status_code != 401:
                response.failure("Got unexpected response code: " + str(response.status_code) + " Error: " + str(response.text))
            else:
                print("401 Test passed")
        response.success() 

    @task(1)
    def purchase(self): 
        #self.client.post(
          #  "/purchasePlaces",
            #data={"places": 5, 
                  #"club": self.club[0]["name"], 
                  #"club": "She Lifts", 
                  #"competition": self.competitions[0]["name"]}, 
                   #"competition": "Spring Festival"},
            #name="/purchasePlaces"
        #)
        with self.client.post("/purchasePlaces", data={"places": 5, 
                  "club": "She Lifts", 
                   "competition": "Spring Festival"}, catch_response=True) as response:
            if response.status_code != 401:
                response.failure("Got unexpected response code: " + str(response.status_code) + " Error: " + str(response.text))
            else:
                print("401 Test passed")
        response.success() 

class WebsiteUser(HttpUser):
    task_set = ProjectPerfTest
    wait_time = between(5, 20)
