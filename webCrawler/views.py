from django.shortcuts import render
import lxml.html
import requests
import json
from django.http import HttpResponse

# Create your views here.
def startApp(request):
	return render(request, 'webCrawler/index.html', {})

def getdata(request):
	print (request.POST['url'])

def likePost(request):
	if request.method == 'GET':
		data = bfs_connected_component(str(request.GET['post_id']), int(request.GET['depthid']))
		print(data)
		return HttpResponse(json.dumps(data), content_type="application/json")

def get_images(url):
	response = requests.get(url)
	tree = lxml.html.fromstring(response.text)
	title_elem = tree.xpath('//img')
	link_list = [each.attrib['src'] for each in title_elem]
	return link_list

def get_links(url):
	response = requests.get(url)
	tree = lxml.html.fromstring(response.text)
	title_elem = tree.xpath('//a')
	link_list = [each.attrib['href'] for each in title_elem]
	return link_list

def bfs_connected_component(start, count):
    dic = {}
    explored = []
    queue = [start]
    flag = 0
    dic["Main URL"] = start
    if count == 1:
        dic[start] = list(set([x for x in get_images(start) if not x.startswith("#")]))
        return dic
    dic["count"] = count
    while queue:
        queue = list(set(queue))
        node = queue.pop(0)
        if flag == count:
            print ("Fetching final images", node)
        print("This is the node we are entering: ", node)
        if node not in explored:
            explored.append(node)
            try:
            	if flag == count:
            		print ("Fetching images: ",node)
            		print (get_images(node))
            		dic['node'] = node
            		dic[node] = get_images(node)
            	else:
            		flag = flag+1
            		neighbours = get_links(node)
            except:
            	pass
 
            if not flag == count:
	            for neighbour in neighbours:
	            	if not neighbour.startswith("/"):
	            		if not neighbour.startswith("#"):
	            			if neighbour.startswith(node.split(".")[0]):
	            				queue.append(neighbour)
    return dic