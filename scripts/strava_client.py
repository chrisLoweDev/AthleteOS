"""
Standalone Strava API client for Athlete OS.
Reads credentials from .env, handles token refresh, fetches activities.
"""

import os
import time
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv, set_key

# Path to the .env file — one directory up from this script
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')


class StravaClient:
    """Standalone Strava API wrapper. No database dependencies."""

    BASE_URL = "https://www.strava.com/api/v3"
    TOKEN_URL = "https://www.strava.com/oauth/token"

    def __init__(self):
        load_dotenv(dotenv_path=ENV_PATH)
        self.client_id = os.getenv('STRAVA_CLIENT_ID')
        self.client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        self.refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
        self.access_token = None

        if not self.client_id or not self.client_secret:
            raise EnvironmentError(
                "STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET must be set in .env"
            )
        if not self.refresh_token:
            raise EnvironmentError(
                "STRAVA_REFRESH_TOKEN is not set in .env. "
                "Run: python scripts/strava_auth.py"
            )

    def refresh_auth_token(self):
        """Exchange refresh token for a new access token. Updates .env with new refresh token."""
        resp = requests.post(self.TOKEN_URL, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        })
        resp.raise_for_status()
        data = resp.json()

        self.access_token = data['access_token']
        new_refresh_token = data['refresh_token']

        # Strava rotates refresh tokens — save the new one immediately
        if new_refresh_token != self.refresh_token:
            self.refresh_token = new_refresh_token
            set_key(ENV_PATH, 'STRAVA_REFRESH_TOKEN', new_refresh_token)

        return data

    def _headers(self):
        if not self.access_token:
            raise RuntimeError("Call refresh_auth_token() before making API requests.")
        return {'Authorization': f'Bearer {self.access_token}'}

    def get_activities_after(self, after_timestamp: int, per_page: int = 100) -> list:
        """
        Fetch all activities after the given Unix timestamp.
        Paginates automatically until no more results.
        """
        activities = []
        page = 1
        request_count = 0

        while True:
            params = {
                'after': after_timestamp,
                'per_page': per_page,
                'page': page,
            }
            resp = requests.get(
                f"{self.BASE_URL}/athlete/activities",
                headers=self._headers(),
                params=params,
            )
            resp.raise_for_status()
            batch = resp.json()
            request_count += 1

            if not batch:
                break

            activities.extend(batch)
            page += 1

            # Rate limit protection: Strava allows 200 requests/15 min
            # Sleep briefly if paginating heavily
            if request_count % 10 == 0:
                print(f"[strava_client] Fetched {len(activities)} activities so far, "
                      f"page {page}...", file=sys.stderr)
                time.sleep(1)

        return activities

    def get_activity_detail(self, activity_id: int) -> dict:
        """Fetch detailed activity data including laps, splits, and segment efforts."""
        resp = requests.get(
            f"{self.BASE_URL}/activities/{activity_id}",
            headers=self._headers(),
            params={'include_all_efforts': True},
        )
        resp.raise_for_status()
        return resp.json()
