from lxml import etree
import re

xml_file = open("input_full_route.xml","r") 

try:
	for _, element in etree.iterparse(xml_file, tag='{http://xml.juniper.net/junos/12.3R8/junos-routing}rt'):
		destination = element.find('{http://xml.juniper.net/junos/12.3R8/junos-routing}rt-destination').text.encode('utf-8')
		prefix_length = element.find('{http://xml.juniper.net/junos/12.3R8/junos-routing}rt-prefix-length').text.encode('utf-8')
		rt_entries = list(element.iter('{http://xml.juniper.net/junos/12.3R8/junos-routing}rt-entry'))
		for rt_entry in rt_entries:
			preference = rt_entry.find('{http://xml.juniper.net/junos/12.3R8/junos-routing}preference').text.encode('utf-8')
			as_path = rt_entry.find('{http://xml.juniper.net/junos/12.3R8/junos-routing}as-path').text.encode('utf-8') ##sonunda gereksiz satir atlama var. 
			###protocol-next hop degerinin bulunmasi
			nhs = list(element.iter('{http://xml.juniper.net/junos/12.3R8/junos-routing}protocol-nh'))
			for nh in nhs: 
				next_hop = nh.find('{http://xml.juniper.net/junos/12.3R8/junos-routing}to').text.encode('utf-8')
				
			###as-path ciktisi 3 satir seklinde, I veya ? oncesindeki degeri alip sonrasinda gobgp ciktisi seklinde duzenlemek 
			as_path = as_path.splitlines()[0] #split lines and take the first one
			
			if "I" in as_path:   
				as_path= as_path.split(" I")[0] #take value before I
			elif "?" in as_path: 
				as_path= as_path.split(" ?")[0] #take value before ? 
			elif "E" in as_path: 
				as_path= as_path.split(" E")[0]	#take value before E 	
			as_path = as_path.split("AS path: ")[-1] # take value after "AS path":
			as_path_list_gogbp_style = '"'+as_path +'"'
			####
			
			if as_path != "" and as_path != "AS path:":
				print "gobgp global rib add -a ipv4 "+destination+"/"+prefix_length+" nexthop "+ next_hop +" local-pref "+ preference +" aspath "+ as_path_list_gogbp_style
			
			element.clear()
except etree.XMLSyntaxError:
	print etree.XMLSyntaxError
