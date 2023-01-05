from playwright.sync_api import expect


def test_sample(session_capabilities) -> None:

    try:
        # Load the PAge returned by the fixture
        page=session_capabilities
        print(page)
        #Navigate to https://bstackdemo.com/
        page.goto("https://bstackdemo.com/", timeout=0)

        #Add the first item to cart
        page.locator("[id=\"\\31 \"]").get_by_text("Add to cart").click()
        phone=page.locator("[id=\"\\31 \"]").locator(".shelf-item__title").all_inner_texts()
        print("Phone =>"+str(phone[0]))

        #Get the items from Cart
        qty=page.locator(".bag__quantity").all_inner_texts()
        print("Bag quantity => "+ str(qty[0]))

        #Verify if there is a shopping cart
        expect(page.locator(".bag__quantity")).to_have_count(1)
        # Verify if there is only one item in the shopping cart
        expect(page.locator(".bag__quantity")).to_have_text("1")

        #Log information to console
        log_contextual_info("The cart has one item","info", page)

        #Get the handle for cart item
        cart_item=page.locator(".shelf-item__details")

        #Verify if the cart has the right item
        expect(cart_item.locator(".title")).to_have_text(phone)

        #Update the test result
        mark_test_status("passed", "The cart has "+str(cart_item.locator(".title").all_inner_texts()[0]), page)
    except Exception as err:
        #Extract error message from Exception
        error=str(err).split("Call log:")[0].replace("\n"," but ").replace(":","=>").replace("'","")
        mark_test_status("failed", error, page)

def mark_test_status(status, reason, page):
  page.evaluate("_ => {}", "browserstack_executor: {\"action\": \"setSessionStatus\", \"arguments\": {\"status\":\""+ status + "\", \"reason\": \"" + reason + "\"}}");

def log_contextual_info(desc,loglevel,page):
    page.evaluate("_ => {}",
                  "browserstack_executor: {\"action\": \"annotate\", \"arguments\": {\"data\":\"" + desc + "\", \"level\": \"" + loglevel + "\"}}");