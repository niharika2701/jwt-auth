import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


# ── Register tests ────────────────────────────────────────────────────────────

class TestRegister:

    def test_register_success(self, page: Page):
        """Valid registration shows success message."""
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "testuser")
        page.fill("#email", "testuser@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Account created")

    def test_register_short_password(self, page: Page):
        """Password under 6 chars shows front-end error."""
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "shortpass")
        page.fill("#email", "shortpass@example.com")
        page.fill("#password", "abc")
        page.fill("#confirm", "abc")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("at least 6 characters")

    def test_register_invalid_email(self, page: Page):
        """Invalid email format shows front-end error."""
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "badmail")
        page.fill("#email", "notanemail")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("valid email")

    def test_register_passwords_dont_match(self, page: Page):
        """Mismatched passwords shows front-end error."""
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "mismatch")
        page.fill("#email", "mismatch@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "different123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("do not match")

    def test_register_duplicate_username(self, page: Page):
        """Duplicate username shows server error."""
        # Register once
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "dupuser")
        page.fill("#email", "dup1@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        page.wait_for_timeout(500)

        # Try again with same username
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "dupuser")
        page.fill("#email", "dup2@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("already taken")


# ── Login tests ───────────────────────────────────────────────────────────────

class TestLogin:

    def test_login_success(self, page: Page):
        """Valid credentials show success message."""
        # Register first
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "loginuser")
        page.fill("#email", "loginuser@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm", "password123")
        page.click("button")
        page.wait_for_timeout(500)

        # Now login
        page.goto(f"{BASE_URL}/login")
        page.fill("#username", "loginuser")
        page.fill("#password", "password123")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Login successful")

    def test_login_wrong_password(self, page: Page):
        """Wrong password shows error message."""
        # Register first
        page.goto(f"{BASE_URL}/register")
        page.fill("#username", "wrongpass")
        page.fill("#email", "wrongpass@example.com")
        page.fill("#password", "correctpassword")
        page.fill("#confirm", "correctpassword")
        page.click("button")
        page.wait_for_timeout(500)

        # Login with wrong password
        page.goto(f"{BASE_URL}/login")
        page.fill("#username", "wrongpass")
        page.fill("#password", "wrongpassword")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Invalid credentials")

    def test_login_unknown_user(self, page: Page):
        """Unknown user shows error message."""
        page.goto(f"{BASE_URL}/login")
        page.fill("#username", "nobody")
        page.fill("#password", "somepassword")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("Invalid credentials")

    def test_login_empty_fields(self, page: Page):
        """Empty username shows front-end error."""
        page.goto(f"{BASE_URL}/login")
        page.click("button")
        expect(page.locator("#message")).to_contain_text("required")