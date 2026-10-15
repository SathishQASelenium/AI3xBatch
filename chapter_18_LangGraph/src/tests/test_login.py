"""The two tests the flaky finder drives.

Both hit the real TTACart login. test_invalid_login is deliberately broken: it
asserts a successful landing after a bad login, so it stays red on every attempt
and the REAL FAILURE branch of the graph is always reachable in a demo.
"""
import re

from playwright.sync_api import Page, expect

URL = "https://app.thetestingacademy.com/playwright/ttacart/"
PASSWORD = "tta_secret"
INVENTORY = re.compile(r"/inventory$")


def login(page: Page, username: str) -> None:
    page.goto(URL)
    page.fill("#user-name", username)
    page.fill("#password", PASSWORD)
    page.click("#login-button")


def test_valid_login(page: Page) -> None:
    login(page, "standard_user")
    expect(page).to_have_url(INVENTORY)


def test_invalid_login(page: Page) -> None:
    login(page, "not_a_real_user")
    expect(page).to_have_url(INVENTORY)
