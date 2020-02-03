from webresourcecrawler import WebResourceCrawler
import sys

if __name__ == "__main__":

  url = sys.argv[1] if len(sys.argv) > 1 else "http://www.zello.com/"
  use_selenium = sys.argv[2] if len(sys.argv) > 2 else False
  crawler = WebResourceCrawler(url)
  res = crawler.run(use_selenium=use_selenium)
  print(res)
