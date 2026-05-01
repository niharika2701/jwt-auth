import pytest
import time
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def unique(base: str) -> str:
    """Generate a unique username using timestamp to avoid DB conflicts."""
    return f"{base}{int(time.time() * 1000) % 100000}"


class TestRegister:

    def test_register_success(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", unique("newuser"))
        page.fill("#email", f"{unique('user')}@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Account created")

    def test_register_short_password(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", unique("shortpass"))
        page.fill("#email", f"{unique('short')}@example.com")
        page.fill("#password", "abc")
        page.fill("#confirm", "abc")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("at least 6 characters")

    def test_register_invalid_email(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", unique("badmail"))
        page.fill("#email", "notanemail")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("valid email")

    def test_register_passwords_dont_match(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", unique("mismatch"))
        page.fill("#email", f"{unique('mis')}@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "different123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("do not match")

    def test_register_duplicate_username(self, page: Page):
        username = unique("dupuser")
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", username)
        page.fill("#email", f"{unique('dup1')}@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        page.wait_for_timeout(500)

        page.goto(f"{BASE_URL}/register")
        page.fill("#username", username)
        page.fill("#email", f"{unique('dup2')}@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("already taken")


class TestLogin:

    def test_login_success(self, page: Page):
        username = unique("loginuser")
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", username)
        page.fill("#email", f"{unique('login')}@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        page.wait_for_timeout(500)

        page.goto(f"{BASE_URL}/login")
        page.fill("#username", username)
        page.fill("#password", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Login successful")

    def test_login_wrong_password(self, page: Page):
        username = unique("wrongpass")
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", username)
        page.fill("#email", f"{unique('wp')}@example.com")
        page.fill("#password", "correctpassword")
        page.fill("#confirm", "correctpassword")
        page.click("button")
        page.wait_for_timeout(500)

        page.goto(f"{BASE_URL}/login")
        page.fill("#username", username)
        page.fill("#password", "wrongpassword")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Invalid credentials")

    def test_login_unknown_user(self, page: Page):
        page.goto(f"{BASE_URL}/login")
        page.fill("#username", "nobody_at_all")
        page.fill("#password", "somepassword")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Invalid credentials")

    def test_login_empty_fields(self, page: Page):
        page.goto(f"{BASE_URL}/login")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("required")