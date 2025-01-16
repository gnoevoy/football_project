x = None

if x is not None:
    print(1)
else:
    print(-1)

    # while True:
    #     html_content = page.content()
    #     soup = BeautifulSoup(html_content, "html.parser")
    #     links = soup.select("a.product-item.product-brick")

    #     for link in links[:1]:
    #         product_links.append(link["href"])

    #     next_page = page.locator("div[class='category-grid__item.last-brick']")

    #     if next_page:
    #         print("found")
    #         page.locator("div[class='category-grid__item.last-brick']").click()
    #     else:
    #         print("not found")
    #         break
