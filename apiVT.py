import vt

async def checkLink(passed_url):
    with open("key.txt", 'r', encoding="utf-8") as fp:
        APIKey = (f"{fp.read()}")

    vtclient = vt.Client(APIKey)
    analysis = await vtclient.scan_url_async(f"{passed_url}", wait_for_completion=True)
    url_id = vt.url_id(passed_url)
    url = await vtclient.get_object_async("/urls/{}", url_id)
    await vtclient.close_async()
    return url.last_analysis_stats