const { test, expect } = require("@playwright/test");

const FRONTEND_URL = "http://127.0.0.1:5173";

test("la aplicación carga correctamente", async ({ page }) => {
    await page.goto(FRONTEND_URL);

    await expect(page.locator("body")).toBeVisible();
});


test("se puede ingresar a Productos", async ({ page }) => {
    await page.goto(FRONTEND_URL);

    await page
        .getByText("Productos", { exact: true })
        .first()
        .click();

    await expect(
        page.getByText("Productos", { exact: true }).first()
    ).toBeVisible();
});


test("se puede ingresar a Materiales", async ({ page }) => {
    await page.goto(FRONTEND_URL);

    await page
        .getByText("Materiales", { exact: true })
        .first()
        .click();

    await expect(
        page.getByText("Materiales", { exact: true }).first()
    ).toBeVisible();
});
