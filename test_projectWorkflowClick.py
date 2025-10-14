import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://word-uat.welocalize.com/project-manager-gui/login.jsp#!/login")
    page.get_by_role("textbox", name="Username").fill("pantheon")
    page.get_by_role("textbox", name="Password").click(modifiers=["ControlOrMeta"])
    page.get_by_role("textbox", name="Password").fill("#Zbb<h5Ec5h&")
    page.get_by_role("button", name="Log in", exact=True).click()
    page.locator("#projectsIframe").content_frame.locator("[id=\"94381496\"]").get_by_role("cell", name="").locator("i").click()
    page.locator("#projectsIframe").content_frame.get_by_role("cell", name="XTM Test Automation team 20251010_185850").click()
    page.locator("#projectsIframe").content_frame.get_by_text("Workflow", exact=True).click()
    page.locator("#projectsIframe").content_frame.locator("#newWorkflowIframe").content_frame.locator("#projecteditorworkIframe").content_frame.get_by_role("button", name="Manage jobs").click()
    page.goto("https://word-uat.welocalize.com/project-manager-gui/logout.jsp?type=LOGGED_OFF_BY_ANOTHER_USER")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
