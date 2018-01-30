f5_pool_member_status.py is a python script that pulls stats of all virtual servers from the F5 load balancer. It'll format the output as a html page to be viewed in a browser. The status of the VIP/Pool/pool member are color-coded :

BLUE = good with question, GRAY = status unknown, GREEN = good, RED = down, YELLOW = disabled

example.png shows an example of the html page.
