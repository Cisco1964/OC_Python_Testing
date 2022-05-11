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
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points":"13"
        }
    ]

    def on_start(self):
        self.client.get('/')
        response = self.client.post('/showSummary', {'email': self.club[0]["email"]})
        print("RESPONSE", response.status_code)
        

    def on_stop(self):
        self.client.get('/logout')


    @task(1)
    def book(self):
        rv = self.client.get(
            #f"/book/{self.competitions[0]['name']}/{self.club[0]['name']}"
            f"/book/SpringFestival/IronTemple"
        )
        print("response1", rv.status_code)
        print("content1", rv.content)

    @task(1)
    def purchase(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club[0]["name"],
                "competition": self.competitions[0]["name"]
            }
        )

class WebsiteUser(HttpUser):
    task_set = ProjectPerfTest
    wait_time = between(5, 20)
