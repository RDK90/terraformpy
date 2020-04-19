from modules.instance_template import InstanceTemplate

#Define variables for instance template here
name="name_of_instance_template"
container="path_to_container_in_registry"
zone="gcp_zone"
tags=["network_tags"]

instance_template = InstanceTemplate(
    name=name,
    container=container,
    zone=zone,
    tags=tags
)