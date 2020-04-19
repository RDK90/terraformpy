from schematics import types
from schematics.types import StringType
from schematics.types.compound import ListType
from terraformpy import Resource, ResourceCollection

class InstanceTemplate(ResourceCollection):

    name = StringType(required=True)
    container = StringType(required=True)
    zone = StringType(required=True)
    tags = ListType(StringType)

    def create_resources(self):
        self.instance_template = Resource(
            "google_compute_instance_template",
            self.name,
            name=self.name,
            machine_type="f1-micro",
            disk={
                "source_image":"cos-cloud/cos-stable-81-12871-69-0",
                "disk_size_gb":5
            },
            metadata={
                "gce-container-declaration":"spec:\n  containers:\n    - name: {}\n      image: '{}'\n      stdin: false\n      tty: false\n  restartPolicy: Always\n".format(self.name, self.container)
            },
            network_interface={
                "network":"development_network",
                "subnetwork":"development_subnet",
                "access_config":{}
            },
            tags=self.tags
        )