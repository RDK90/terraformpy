from schematics import types
from schematics.types import StringType
from schematics.types.compound import ListType
from terraformpy import Resource, ResourceCollection
from modules.managed_instance_group import ManagedInstanceGroup

class ApplicationLoadBalancer(ResourceCollection):

    name = StringType(required=True)
    managed_instance_group = StringType(required=True)
    health_check = StringType(required=True)

    def create_external_ip_address(self):
        self.global_ip_address_name = self.name + "-ip-address"
        self.global_ip_address = Resource(
            "google_compute_global_address",
            self.global_ip_address_name,
            name=self.global_ip_address_name
        )

    def create_backend_service(self):
        self.backend_service_name = self.name + "-backend-service"
        self.backend_service = Resource(
            "google_compute_backend_service",
            self.backend_service_name,
            name=self.backend_service_name,
            health_checks=[self.health_check],
            backend={
                "group":self.managed_instance_group
            }
        )

    def create_url_map(self):
        self.url_map_name = self.name + "-url-map"
        self.url_map = Resource(
            "google_compute_url_map",
            self.url_map_name,
            name=self.url_map_name,
            default_service=self.backend_service.self_link
        )

    def create_http_proxy(self):
        self.http_proxy_name = self.name + "-http-proxy"
        self.http_proxy = Resource(
            "google_compute_target_http_proxy",
            self.http_proxy_name,
            name=self.http_proxy_name,
            url_map=self.url_map.self_link
        )

    def create_frontend_service(self):
        self.frontend_service_name = self.name + "-frontend-service"
        self.frontend_service = Resource(
            "google_compute_global_forwarding_rule",
            self.frontend_service_name,
            name=self.frontend_service_name,
            target=self.http_proxy.self_link,
            port_range="8080",
            load_balancing_scheme="EXTERNAL",
            ip_address=self.global_ip_address.address
        )
    
    def create_resources(self):
        self.create_external_ip_address(self)
        self.create_backend_service(self)
        self.create_url_map(self)
        self.create_http_proxy(self)
        self.create_frontend_service(self)
        
