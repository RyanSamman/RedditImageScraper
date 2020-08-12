import re
import shutil
import requests


def main():
	REDDIT_PAGE_URL = 'https://old.reddit.com/r/liminalspace'

	html = retrieveHtml(REDDIT_PAGE_URL)
	imageElements = getImageElements(html)
	print(*imageElements, sep='\n')
	#postImageElements = filterPostElements(imageElements)
	urls = [getSrcFromElement(i) for i in imageElements]
	deampedUrls = [deampUrl(u) for u in urls]

	print(*deampedUrls, sep="\n")

	[downloadImage(img_url, i) for i, img_url in enumerate(deampedUrls)]


def retrieveHtml(url):
	# May not be needed (Used to simulate the browser)
	fakeBrowserHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
	res = requests.get(url, headers=fakeBrowserHeader)
	# If you ever need to get key/value pair off cookies:
	# cookies = {c.name:c.value for c in res.cookies}
	assert res.status_code == 200
	return res.text


def getImageElements(html):
	return re.findall("<img.*?>", html)


def filterPostElements(images):
	return [img for img in images if re.findall("Post image", img)]


def getSrcFromElement(imageElement):
	src = re.findall(r'<img.*?src="(.*?)"', imageElement)[0]
	# TODO: Append base URL for relative paths, ex. '/img' instead of 'https://reddit.com/image'
	return src


def deampUrl(url):
	return url.replace('amp;', '')


def downloadImage(url, i=0):
	res = None
	try:
		res = requests.get(url, stream=True)
	except requests.exceptions.MissingSchema:
		res = requests.get(f"https://{url[2:]}", stream=True)
	finally:
		if res.status_code != 200:
			print(f"Image #{i} ({url}) has a status of {res.status_code}!\nAborting!")
			return

		with open(f'{i}.png', 'wb') as out_file:
			shutil.copyfileobj(res.raw, out_file)


if __name__ == "__main__":
	main()