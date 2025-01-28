from typing import Any
import unittest
from src.unmonitorr.types_ import (
    RadarrWebhookPayload,
    SonarrWebhookPayload,
    WebhookEpisode,
)


class TestTestPayloads(unittest.TestCase):
    def test_valid_radarr_test_payload(self) -> None:
        payload: dict[str, Any] = {
            "movie": {
                "id": 1,
                "title": "Test Title",
                "year": 1970,
                "releaseDate": "1970-01-01",
                "folderPath": "C:\\testpath",
                "tmdbId": 0,
                "tags": ["test-tag"],
            },
            "remoteMovie": {"tmdbId": 1234, "imdbId": "5678", "title": "Test title", "year": 1970},
            "release": {
                "quality": "Test Quality",
                "qualityVersion": 1,
                "releaseGroup": "Test Group",
                "releaseTitle": "Test Title",
                "indexer": "Test Indexer",
                "size": 9999999,
                "customFormatScore": 0,
            },
            "eventType": "Test",
            "instanceName": "Radarr",
            "applicationUrl": "",
        }

        radarr_payload = RadarrWebhookPayload.model_validate(payload)

        self.assertEqual(radarr_payload.movie.title, "Test Title")
        self.assertEqual(radarr_payload.movie.year, 1970)
        self.assertEqual(radarr_payload.event_type, "Test")

    def test_valid_sonarr_test_payload(self) -> None:
        payload: dict[str, Any] = {
            "series": {
                "id": 1,
                "title": "Test Title",
                "path": "C:\\testpath",
                "tvdbId": 1234,
                "tvMazeId": 0,
                "tmdbId": 0,
                "type": "standard",
                "year": 0,
                "tags": ["test-tag"],
            },
            "episodes": [
                {
                    "id": 123,
                    "episodeNumber": 1,
                    "seasonNumber": 1,
                    "title": "Test title",
                    "seriesId": 0,
                    "tvdbId": 0,
                }
            ],
            "eventType": "Test",
            "instanceName": "Sonarr",
            "applicationUrl": "",
        }

        sonarr_test_payload = SonarrWebhookPayload.model_validate(payload)

        self.assertEqual(sonarr_test_payload.event_type, "Test")
        self.assertEqual(sonarr_test_payload.series.title, "Test Title")
        self.assertEqual(sonarr_test_payload.series.id, 1)
        self.assertEqual(sonarr_test_payload.episodes[0].id, 123)
        self.assertTrue(
            all(isinstance(episode, WebhookEpisode) for episode in sonarr_test_payload.episodes)
        )


if __name__ == "__main__":
    unittest.main()
