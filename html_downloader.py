# -*- coding: UTF-8 -*-   

import urllib.request

class HtmlDownloader(object):
	

    def download(self,url):
        if url is None:
            return None
        count = 0
        while True:
            try:
                response = urllib.request.urlopen(url)
                if response.getcode()==200:
                    break
                else:
                    raise WebError
            except urllib.error.HTTPError as err:
                if err.code != 404:
                    pass
                else:
                    count = count + 1
                    if count == 5:
                        print ('\titjuzi 404 error for '+url)
                        return '404'
        return response.read()
