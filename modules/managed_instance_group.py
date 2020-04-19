from schematics import types
from schematics.types import StringType
from schematics.types.compound import ListType
from terraformpy import Resource, ResourceCollection
from modules.instance_template import InstanceTemplate

class ManagedInstanceGroup(ResourceCollection):

    name = StringType(required=True)
    zone = StringType(required=True)
    tags = ListType(StringType, required=True)
    container = StringType(required=True)

    def create_instance_template(self):
        self.instance_template_name = self.name + "-template"
        self.instance_template = InstanceTemplate(
            name=self.instance_template_name,
            container=self.container,
            zone=self.zone,
            tags=self.tags
        )

    def create_health_check(self):
        self.health_check_name = self.instance_template + "-health-check"
        self.health_check = Resource(
            "google_compute_health_check",
            self.health_check_name,
            name=self.health_check_name,
            check_interval_sec=10,
            timeout_sec=10,
            healthy_threshold=3,
            unhealthy_threshold=3,
            http_health_check={
                "request_path":"/api/v1/healthcheck",
                "port":8080
            }
        )

    def create_managed_instance_group(self):
        self.managed_instance_group_name = self.instance_template + "-group"
        self.managed_instance_group = Resource(
            "google_compute_instance_group_manager",
            self.managed_instance_group_name,
            name=self.managed_instance_group_name,
            base_instance_name=self.instance_template.name,
            zone=self.zone,
            version={
                "instance_template":self.instance_template.self_link,
                "initial_delay_sec":180
            }
        )

    def create_autoscaler(self):
        self.autoscaler_name = self.instance_template + "-autoscaler"
        self.autoscaler = Resource(
            "google_compute_autoscaler",
            self.autoscaler_name,
            name=self.autoscaler_name,
            zone=self.zone,
            target=self.managed_instance_group.id,
            autoscaling_policy={
                "max_replicas":5,
                "min_replicas":2,
                "cooldown_period":60,
                "cpu_utilization":{
                    "target":0.75
                }
            }
        )

    def create_resources(self):
        self.create_instance_template(self)
        self.create_health_check(self)
        self.create_managed_instance_group(self)
        self.create_autoscaler(self)

