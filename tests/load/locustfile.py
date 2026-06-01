from locust import HttpUser, between, task


class ResearchAgentUser(HttpUser):
    wait_time = between(0.1, 1.0)

    @task(8)
    def cached_google_query(self) -> None:
        self.client.get("/api/v1/query", params={"q": "Should I buy Google now?"})

    @task(2)
    def varied_query(self) -> None:
        self.client.get(
            "/api/v1/query",
            params={"q": "What are the risks for Microsoft after earnings?"},
        )
