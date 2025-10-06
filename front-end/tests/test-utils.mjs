/**
 * Common test actions for Playwright tests
 */

import { expect } from "@playwright/test";

/**
 * Log in with sample credentials
 * @param {import('@playwright/test').Page} page
 */
export async function loginAsSample(page) {
  await page.goto("/");
  await page.fill('[data-form="login"] input[name="username"]', "sample");
  await page.fill('[data-form="login"] input[name="password"]', "sosecret");
  await page.click('[data-form="login"] [data-submit]');
}

/**
 * Log in with sample credentials
 * @param {import('@playwright/test').Page} page
 */
export async function loginAsJustSomeGuy(page) {
  await page.goto("/");
  await page.fill('[data-form="login"] input[name="username"]', "JustSomeGuy");
  await page.fill('[data-form="login"] input[name="password"]', "mysterious");
  await page.click('[data-form="login"] [data-submit]');
}

/**
 * Log in with sample credentials
 * @param {import('@playwright/test').Page} page
 */
export async function loginAsSwiz(page) {
  await page.goto("/");
  await page.fill('[data-form="login"] input[name="username"]', "Swiz");
  await page.fill(
    '[data-form="login"] input[name="password"]',
    "singingalldayeveryday"
  );
  await page.click('[data-form="login"] [data-submit]');
}

/**
 * Sign up with generated credentials
 * @param {import('@playwright/test').Page} page
 * @param {string} username - Username to sign up with
 */
export async function signUp(page, username) {
  await page.goto("/#/signup");
  await page.fill('[data-form="signup"] input[name="username"]', username);
  await page.fill('[data-form="signup"] input[name="password"]', "sosecret");
  await page.fill(
    '[data-form="signup"] input[name="password_confirmation"]',
    "sosecret"
  );
  await page.click('[data-form="signup"] [data-submit]');
}

/**
 * Post a bloom
 * @param {import('@playwright/test').Page} page
 * @param {string} content - Bloom content
 */
export async function postBloom(page, content) {
  // Added timeouts here because tests try to fill textarea before the whole page loaded
  await page.waitForTimeout(400);
  await page.fill('[data-form="bloom"] textarea[name="content"]', content);
  await page.waitForTimeout(200);
  await page.click('[data-form="bloom"] [data-submit]');
}

/**
 * Log out the current user
 * @param {import('@playwright/test').Page} page
 */
export async function logout(page) {
  await page.click("[data-logout-button]");
}

/**
 * Generate a unique username for testing
 * @returns {string} Unique username
 */
export function generateUsername() {
  return `testuser_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
}

export const TIMELINE_USERNAMES_ELEMENTS_LOCATOR =
  "#timeline-container article [data-username]";

export const waitForLocatorToHaveMatches = async (page, locator) =>
  await expect.poll(() => page.locator(locator).count()).toBeGreaterThan(0);
