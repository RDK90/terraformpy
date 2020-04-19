from terraformpy import Provider

#Define project and region in the variables below
project="define_project_here"
region="define_region_here"

Provider(
    "google",
    project=project,
    region=region
)