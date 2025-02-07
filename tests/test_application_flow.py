from playwright.sync_api import Page, expect
import pytest

import subprocess
import time
import requests
import re

@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""

    proc = subprocess.Popen(["python3", "app.py"])

    for _ in range(50):
        try:
            response = requests.get("http://localhost:5000/thanks", timeout=1)
            if response.status_code == 200:
                break
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.2)
    else:
        raise RuntimeError("Failed to start Flask server")

    page.goto("http://localhost:5000/clear-applicants")
    yield

    proc.terminate()
    proc.wait()


def test_clear(page: Page):
    """Confirm that output text is visible"""

    row_count = page.locator('tbody tr').count()
    assert row_count == 0

def test_docx_upload(page: Page):
    # Navigate to the apply page
    page.goto("http://localhost:5000/apply")
    
    # Fill in the name field
    page.fill('input[name="name"]', 'Test Applicant')
    
    # Upload the file
    page.set_input_files('input[type="file"]', 'example.docx')
    
    # Submit the form
    page.click('input[type="submit"]', timeout=180000)
    
    # Check if the page redirects to a success page or shows a success message
    expect(page).to_have_url("http://localhost:5000/thanks", timeout=180000)
    expect(page.locator('body')).to_contain_text("Thank you")

    page.goto("http://localhost:5000/applicants")
    expect(page.locator('body')).to_contain_text("- Network Engineer, Raytheon, (2015-present)")
    expect(page.locator('body')).to_contain_text(re.compile(r"Grade [ABCD]"))
