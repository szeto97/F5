#!/usr/bin/env python
import sys
import bigsuds
import socket

def prepare_html():
	print "<!DOCTYPE html>"
	print "<html>"
	print "<head>"
	print "<style>"
	print "green {"
	print "    color: #008000;"
	print "}"
	print "red {"
	print "    color: #ff0000;"
	print "}"
	print "yellow {"
	print "    color: #FACC2E;"
	print "}"
	print "gray {"
	print "    color: #808080;"
	print "}"
	print "blue {"
	print "    color: #0000FF;"
	print "}"
	print "table, th, td {"
	print "    border: 1px solid black;"
	print "    border-collapse: collapse;"
	print "    text-align: center;"
	print "    font-family: Arial; font-size: 8pt;"
	print "    table-layout:fixed;"
	print "}"
	print "th, td {"
	print "    padding: 2px;"
	print "}"
	print "button.accordion {"
	print "    background-color: #eee;"
	print "    color: #444;"
	print "    cursor: pointer;"
	print "    padding: 10px;"
	print "    width: 100%;"
	print "    border: none;"
	print "    text-align: left;"
	print "    outline: none;"
	print "    font-size: 14px;"
	print "    transition: 0.4s;"
	print "}"

	print "button.accordion.active, button.accordion:hover {"
	print "    background-color: #ccc;"
	print "}"

	print "div.panel {"
	print "    padding: 0 18px;"
	print "    display: yes;"
	print "    background-color: white;"
	print "}"
	print "</style>"
	print "</head>"
	print "<body>"
	print ""

def lookup_color(status):
	colors = [{'AVAILABILITY_STATUS_GREEN': '<green>AVAILABILITY_STATUS_GREEN&#10004;</green>', 'AVAILABILITY_STATUS_RED': '<red>AVAILABILITY_STATUS_RED&#10008;</red>', 'AVAILABILITY_STATUS_BLUE': '<blue>AVAILABILITY_STATUS_BLUE</blue>', 'ENABLED_STATUS_ENABLED': '<green>ENABLED_STATUS_ENABLED&#10004;</green>', 'ENABLED_STATUS_DISABLED': '<yellow>ENABLED_STATUS_DISABLED</yellow>'}]
	unknown_status_color = '<gray>unknown</gray>'

	try:
		color_status = colors[0][status]
		return color_status
	except Exception, e:
		return unknown_status_color

def end_html():
	print '<script>'
	print 'var acc = document.getElementsByClassName("accordion");'
	print 'var i;'
	print ''
	print 'for (i = 0; i < acc.length; i++) {'
	print '    acc[i].onclick = function(){'
        print '        this.classList.toggle("active");'
        print '        var panel = this.nextElementSibling;'
        print '        if (panel.style.display === "block") {'
        print '            panel.style.display = "none";'
        print '        } else {'
        print '            panel.style.display = "block";'
	print '        }'
	print '    }'
	print '}'
	print '</script>'
	print ''
	print '</body>'
	print '</html>'

def get_virtual_servers(obj):
	try:
		return obj.LocalLB.VirtualServer.get_list()
	except Exception, e:
		print e

def get_virtual_server_status(obj,vs):
	try:
		return obj.LocalLB.VirtualServer.get_object_status([vs])
	except Exception, e:
		print e

def get_virtual_server_persistence_profile(obj,vs):
	try:
		return obj.LocalLB.VirtualServer.get_persistence_profile([vs])
	except Exception, e:
		print e

def get_virtual_server_fallback_persistence_profile(obj,vs):
	try:
		return obj.LocalLB.VirtualServer.get_fallback_persistence_profile([vs])
	except Exception, e:
		print e

def get_virtual_server_dest_address(obj,vs):
	try:
		return obj.LocalLB.VirtualServer.get_destination_v2([vs])
	except Exception, e:
		print e

def get_virtual_server_default_pool_name(obj,vs):
	try:
		return obj.LocalLB.VirtualServer.get_default_pool_name([vs])
	except Exception, e:
		print e
 
def get_status(obj, pool):
	try:
		return obj.LocalLB.Pool.get_member_session_status(pool)
	except Exception, e:
		print e

def get_hostname(address):
	try:
		return socket.gethostbyaddr(address)[0]
	except:
		return address

try:
	b = bigsuds.BIGIP(
	hostname = "my-f5-host",
	username = "my-f5-username",
	password = "my-f5-password",
	)
except Exception, e:
	print e

prepare_html()

virtualservers = get_virtual_servers(b)

for vs in virtualservers:
	vs_name = vs.replace('/Common/','')
	vs_status = get_virtual_server_status(b,vs)
	vs_status_color = lookup_color(vs_status)
	vs_availability_status = vs_status[0]['availability_status']
	vs_availability_status_color = lookup_color(vs_availability_status)
	vs_enabled_status = vs_status[0]['enabled_status']
	vs_enabled_status_color = lookup_color(vs_enabled_status)
	vs_status_description = vs_status[0]['status_description']
	vs_persistence_profile = get_virtual_server_persistence_profile(b,vs)
	if len(vs_persistence_profile[0]) > 0:
		vs_persistence_profile_name = vs_persistence_profile[0][0]['profile_name'].replace('/Common/','')
	else:
		vs_persistence_profile_name = 'None'
	vs_fallback_persistence_profile = get_virtual_server_fallback_persistence_profile(b,vs)
	if vs_fallback_persistence_profile:
		vs_fallback_persistence_profile_name = vs_fallback_persistence_profile[0].replace('/Common/','')
	else:
		vs_fallback_persistence_profile_name = 'None'

	vs_address = get_virtual_server_dest_address(b,vs)
	vs_address_port = vs_address[0]['port']
	vs_address_ip = vs_address[0]['address'].replace('/Common/','')

	if len(vs_address_ip) < 3:
		vs_address_ip = ''

	vs_name = vs.replace('/Common/','')

	print '<!--<button class="accordion"><pre>VIP Name : %s\tIP: %s\tPort: %s"</pre></button>-->' % (vs_name,vs_address_ip,vs_address_port)
	print '<button class="accordion">'
	print '<table style="width: 80%; border; padding: 5px; text-align: left;">'
	print '  <tr>'
	print '    <td>VIP Name : %s</td>' % (vs_name)
	print '    <td>IP: %s</td>' % (vs_address_ip)
	print '    <td>Port: %s</td>' % (vs_address_port)
	print '  </tr>'
	print '</table>'
	print '</button>'
	print '<div class="panel">'
	print '<br>'
	print '<table>'
	print '  <tr>'
	print '    <th>Availability Status</th>'
	print '    <th>Enable Status</th>'
	print '    <th>Status Description</th>'
	print '    <th>Persistence Profile</th>'
	print '    <th>Fallback Persistence Profile</th>'
	print '  </tr>'
	print '  <tr>'
	print '    <td>%s</td>' % (vs_availability_status_color)
	print '    <td>%s</td>' % (vs_enabled_status_color)
	print '    <td>%s</td>' % (vs_status_description)
	print '    <td>%s</td>' % (vs_persistence_profile_name)
	print '    <td>%s</td>' % (vs_fallback_persistence_profile_name)
	print '  </tr>'
	print '</table>'

	pool = get_virtual_server_default_pool_name(b,vs)
	if pool[0]:
		pool_name = pool[0].replace('/Common/','')
		lbmethod = b.LocalLB.Pool.get_lb_method([pool])
		lbmethod_str = str(lbmethod).replace('[','').replace(']','').replace("'","").replace('LB_METHOD_','')
		print '    <h3><pre>Pool Name: %s          LB Method: %s</pre></h3>' % (pool_name, lbmethod_str)
		members = b.LocalLB.Pool.get_member_v2([pool])
		object_status = b.LocalLB.Pool.get_member_object_status([pool], members)
		member_address = b.LocalLB.Pool.get_member_address([pool], members)
		print '    Pool Members:'

		for members, object_status, member_address in zip(members, object_status, member_address):
			count = 0
			print '<table>'
			print '  <tr>'
			print '    <th>Name</th>'
			print '    <th>Server Name / IP</th>'
			print '    <th>Port</th>'
			print '    <th>Availability Status</th>'
			print '    <th>Enable Status</th>'
			print '    <th>Status Description</th>'
			print '    <th>Current Connections</th>'
			print '  </tr>'

			while count < len(members):
				member_port = members[count]['port']
				member_name = members[count]['address'].replace('/Common/','')
				member_statistics = b.LocalLB.Pool.get_member_statistics([pool], [[members[count]]])
				str_member_address = str(member_address[count]).replace('[[','').replace(']]','').replace("'","")
				member_dns_name = get_hostname(str_member_address)
				availability_status = object_status[count]['availability_status']
				availability_status_color = lookup_color(availability_status)
				enabled_status = object_status[count]['enabled_status']
				enabled_status_color = lookup_color(enabled_status)
				status_description = object_status[count]['status_description']
				current_connections = member_statistics[0]['statistics'][0]['statistics'][4]['value']['low']
				print '  <tr>'
				print '    <td>%s</td>' % (member_name)
				print '    <td>%s</td>' % (member_dns_name)
				print '    <td>%s</td>' % (member_port)
				print '    <td>%s</td>' % (availability_status_color)
				print '    <td>%s</td>' % (enabled_status_color)
				print '    <td>%s</td>' % (status_description)
				print '    <td style="text-align:center">%s</td>' % (current_connections)
				print '  </tr>'
				count += 1
			print '</table>'
			print '</div>'
	else:
		print '</div>'

end_html()
