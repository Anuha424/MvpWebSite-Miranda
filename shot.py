from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel=None, executable_path="/root/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width":1440,"height":900})
    errs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto("http://localhost:4173/", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    # force reveal all
    pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
    pg.wait_for_timeout(600)
    pg.screenshot(path="shot_top.png")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight*0.28)")
    pg.wait_for_timeout(800)
    pg.screenshot(path="shot_banner.png")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight*0.55)")
    pg.wait_for_timeout(800)
    pg.screenshot(path="shot_grid.png")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(800)
    pg.screenshot(path="shot_bottom.png")
    # menu overlay
    pg.evaluate("window.scrollTo(0,0)")
    pg.click("#menu-btn")
    pg.wait_for_timeout(900)
    pg.screenshot(path="shot_menu.png")
    print("console errors:", errs[:5])
    b.close()
