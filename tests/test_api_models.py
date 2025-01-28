from typing import Any
import unittest

from src.unmonitorr.types_ import SonarrAPISeries, RadarrAPIMovie


class TestAPIModels(unittest.TestCase):
    def setUp(self) -> None:
        self.radarr_api_payload: dict[str, Any] = {
            "title": "Bill Burr: I'm Sorry You Feel That Way",
            "originalTitle": "Bill Burr: I'm Sorry You Feel That Way",
            "originalLanguage": {"id": 1, "name": "English"},
            "alternateTitles": [],
            "secondaryYearSourceId": 0,
            "sortTitle": "bill burr i m sorry you feel that way",
            "sizeOnDisk": 1311268683,
            "status": "released",
            "overview": "Fresh, unflinching and devastatingly honest, Bill Burr lets loose in this feature length comedy special. Burr shares his essential tips for surviving the zombie apocalypse, exposes how rom-coms ruin great sex and explains how too many childhood hugs may be the ultimate downfall of man.",
            "digitalRelease": "2014-12-05T00:00:00Z",
            "releaseDate": "2014-12-05T00:00:00Z",
            "images": [
                {
                    "coverType": "poster",
                    "url": "/MediaCover/2936/poster.jpg?lastWrite=638412345505555528",
                    "remoteUrl": "https://image.tmdb.org/t/p/original/abpDJ3XyqSp0sQdG7SIAItjBHb1.jpg",
                },
                {
                    "coverType": "fanart",
                    "url": "/MediaCover/2936/fanart.jpg?lastWrite=638412345506655620",
                    "remoteUrl": "https://image.tmdb.org/t/p/original/9rPXzn4QrtGQQIi31FCWil4ohCO.jpg",
                },
            ],
            "website": "",
            "year": 2014,
            "youTubeTrailerId": "eGC1cUyYXHo",
            "studio": "New Wave Entertainment Television",
            "path": "/media/Comedy/Bill Burr - I'm Sorry You Feel That Way (2014)",
            "qualityProfileId": 7,
            "hasFile": True,
            "movieFileId": 4532,
            "monitored": True,
            "minimumAvailability": "announced",
            "isAvailable": True,
            "folderName": "/media/Comedy/Bill Burr - I'm Sorry You Feel That Way (2014)",
            "runtime": 80,
            "cleanTitle": "billburrimsorryyoufeelthatway",
            "imdbId": "tt3823690",
            "tmdbId": 308571,
            "titleSlug": "308571",
            "rootFolderPath": "/media/Comedy/",
            "genres": ["Comedy"],
            "tags": [],
            "added": "2021-03-22T14:59:23Z",
            "ratings": {
                "imdb": {"votes": 9250, "value": 8.2, "type": "user"},
                "tmdb": {"votes": 144, "value": 7.6, "type": "user"},
                "rottenTomatoes": {"votes": 0, "value": 100, "type": "user"},
                "trakt": {"votes": 772, "value": 8.00777, "type": "user"},
            },
            "movieFile": {
                "movieId": 2936,
                "relativePath": "Bill Burr I'm Sorry You Feel That Way (2014).mkv",
                "path": "/media/Comedy/Bill Burr - I'm Sorry You Feel That Way (2014)/Bill Burr I'm Sorry You Feel That Way (2014).mkv",
                "size": 1311268683,
                "dateAdded": "2021-03-22T14:59:42Z",
                "edition": "",
                "languages": [{"id": 1, "name": "English"}],
                "quality": {
                    "quality": {
                        "id": 3,
                        "name": "WEBDL-1080p",
                        "source": "webdl",
                        "resolution": 1080,
                        "modifier": "none",
                    },
                    "revision": {"version": 1, "real": 0, "isRepack": False},
                },
                "customFormatScore": 0,
                "indexerFlags": 0,
                "mediaInfo": {
                    "audioBitrate": 0,
                    "audioChannels": 2,
                    "audioCodec": "AAC",
                    "audioLanguages": "eng",
                    "audioStreamCount": 1,
                    "videoBitDepth": 8,
                    "videoBitrate": 0,
                    "videoCodec": "h265",
                    "videoFps": 23.976,
                    "videoDynamicRange": "",
                    "videoDynamicRangeType": "",
                    "resolution": "1920x1080",
                    "runTime": "1:20:38",
                    "scanType": "Progressive",
                    "subtitles": "",
                },
                "qualityCutoffNotMet": True,
                "id": 4532,
            },
            "popularity": 5.566,
            "statistics": {"movieFileCount": 1, "sizeOnDisk": 1311268683, "releaseGroups": []},
            "id": 2936,
        }

        self.sonarr_api_payload: dict[str, Any] = {
            "title": "Agatha All Along",
            "alternateTitles": [
                {"title": "Agatha ¿quién si no?", "seasonNumber": -1},
                {"title": "Agatha quién si no", "seasonNumber": -1},
                {"title": "Agatha quien si no", "seasonNumber": -1},
                {"title": "To zawsze Agatha / Agatha All Along", "seasonNumber": -1},
            ],
            "sortTitle": "agatha all along",
            "status": "ended",
            "ended": True,
            "overview": "The infamous Agatha Harkness finds herself down and out of power after a suspicious goth Teen helps break her free from a distorted spell. Her interest is piqued when he begs her to take him on the legendary Witches' Road, a magical gauntlet of trials that, if survived, rewards a witch with what they're missing. Together, Agatha and this mysterious Teen pull together a desperate coven, and set off down, down, down The Road...",
            "network": "Disney+",
            "airTime": "21:00",
            "images": [
                {
                    "coverType": "banner",
                    "url": "/MediaCover/874/banner.jpg?lastWrite=638602238424765532",
                    "remoteUrl": "https://artworks.thetvdb.com/banners/v4/series/412429/banners/668ccb09ba2a5.jpg",
                },
                {
                    "coverType": "poster",
                    "url": "/MediaCover/874/poster.jpg?lastWrite=638635697286533083",
                    "remoteUrl": "https://artworks.thetvdb.com/banners/v4/series/412429/posters/66dd63275dc04.jpg",
                },
                {
                    "coverType": "fanart",
                    "url": "/MediaCover/874/fanart.jpg?lastWrite=638635697286983089",
                    "remoteUrl": "https://artworks.thetvdb.com/banners/v4/series/412429/backgrounds/66dd1735382c6.jpg",
                },
                {
                    "coverType": "clearlogo",
                    "url": "/MediaCover/874/clearlogo.png?lastWrite=638602238425845548",
                    "remoteUrl": "https://artworks.thetvdb.com/banners/v4/series/412429/clearlogo/66618021a394c.png",
                },
            ],
            "originalLanguage": {"id": 1, "name": "English"},
            "seasons": [
                {
                    "seasonNumber": 1,
                    "monitored": True,
                    "statistics": {
                        "episodeFileCount": 9,
                        "episodeCount": 9,
                        "totalEpisodeCount": 9,
                        "sizeOnDisk": 4196630320,
                        "releaseGroups": ["FLU", "FLUX", "NHTFS", "SuccessfulCrab"],
                        "percentOfEpisodes": 100,
                    },
                }
            ],
            "year": 2024,
            "path": "/media/TV Shows/Agatha All Along",
            "qualityProfileId": 7,
            "seasonFolder": True,
            "monitored": True,
            "monitorNewItems": "all",
            "useSceneNumbering": False,
            "runtime": 40,
            "tvdbId": 412429,
            "tvRageId": 0,
            "tvMazeId": 58948,
            "tmdbId": 138501,
            "firstAired": "2024-09-18T00:00:00Z",
            "lastAired": "2024-10-30T00:00:00Z",
            "seriesType": "standard",
            "cleanTitle": "agathaallalong",
            "imdbId": "tt15571732",
            "titleSlug": "agatha-all-along",
            "rootFolderPath": "/media/TV Shows",
            "certification": "TV-14",
            "genres": [
                "Action",
                "Adventure",
                "Comedy",
                "Fantasy",
                "Mini-Series",
                "Science Fiction",
            ],
            "tags": [],
            "added": "2024-08-25T23:04:02Z",
            "ratings": {"votes": 0, "value": 0},
            "statistics": {
                "seasonCount": 1,
                "episodeFileCount": 9,
                "episodeCount": 9,
                "totalEpisodeCount": 9,
                "sizeOnDisk": 4196630320,
                "releaseGroups": ["FLU", "FLUX", "NHTFS", "SuccessfulCrab"],
                "percentOfEpisodes": 100,
            },
            "languageProfileId": 1,
            "id": 874,
        }

    def test_valid_radarr_api_movie(self) -> None:
        movie = RadarrAPIMovie.model_validate(self.radarr_api_payload)

        self.assertEqual(movie.id, 2936)
        self.assertEqual(movie.title, "Bill Burr: I'm Sorry You Feel That Way")
        self.assertEqual(movie.monitored, True)

    def test_valid_sonarr_api_series(self) -> None:
        series = SonarrAPISeries.model_validate(self.sonarr_api_payload)

        self.assertEqual(series.id, 874)
        self.assertEqual(series.title, "Agatha All Along")
        self.assertEqual(series.monitored, True)
        self.assertEqual(series.status, "ended")
        self.assertEqual(series.is_complete, True)

        series.unmonitor_series()

        self.assertEqual(series.monitored, False)

    def test_radarr_api_model_dump(self) -> None:
        """Validate the the dumped radarr model matches the original."""
        movie = RadarrAPIMovie.model_validate(self.radarr_api_payload)
        movie_data = movie.model_dump(by_alias=True)

        self.assertEqual(movie_data, self.radarr_api_payload)

    def test_sonarr_api_model_dump(self) -> None:
        """Validate the the dumped sonarr model matches the original."""
        series = SonarrAPISeries.model_validate(self.sonarr_api_payload)
        series_data = series.model_dump(by_alias=True)

        self.assertEqual(series_data, self.sonarr_api_payload)


if __name__ == "__main__":
    unittest.main()
