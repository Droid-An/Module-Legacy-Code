import { test, expect } from "@playwright/test";
import {
  TIMELINE_USERNAMES_ELEMENTS_LOCATOR,
  loginAsSample,
  loginAsJustSomeGuy,
  loginAsSwiz,
  waitForLocatorToHaveMatches,
  signUp,
  logout,
  postBloom,
} from "./test-utils.mjs";

test.describe("Rebloom functionality", () => {
  test("'Share' button is visible", async ({ page }) => {
    // Given I am logged in as sample
    await loginAsSample(page);
    // When I go to AS profile
    await page.goto("/#/profile/AS");
    // Then I see a "Share "button
    const shareButton = page.locator('[data-action="share-bloom"]');
    await expect(shareButton).toBeVisible();
  });

  test("Follower see your new post in their's home view", async ({ page }) => {
    // Given I am logged in as sample
    await loginAsSample(page);

    // When I create a bloom
    await postBloom(page, "My 666 bloom!");

    // Then I see the bloom in the timeline
    await expect(
      page.locator("[data-bloom] [data-content]").first()
    ).toContainText("My 666 bloom!");

    // When I logout
    await logout(page);

    // When I am logged in as Swiz who already follows Sample
    await loginAsSwiz(page);

    // Then I see the sample's bloom in the timeline
    await expect(
      page.locator("[data-bloom] [data-content]").first()
    ).toContainText("My 666 bloom!");
  });

  test("Rebloom count updates, when click share", async ({ page }) => {
    // Given I am logged in as sample
    await loginAsSample(page);

    await postBloom(page, "My 666 bloom!");

    await logout(page);

    // When I am logged in as Swiz who already follows Sample
    await loginAsSwiz(page);

    await page.click(`[data-action="share-bloom"]`);
    await page.waitForTimeout(200);
    const rebloomCount = page.locator("[data-rebloom-count]").nth(1);
    await page.waitForTimeout(200);
    await expect(rebloomCount).toHaveText("1");
  });
});
