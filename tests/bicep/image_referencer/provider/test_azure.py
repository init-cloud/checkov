from networkx import DiGraph

from checkov.common.images.image_referencer import Image
from checkov.terraform.image_referencer.provider.azure import AzureTerraformProvider


def extract_images_from_resources():
    # given
    resource = {
        "file_path_": "/batch.bicep",
        "__end_line__": 26,
        "__start_line__": 1,
        "properties": {
            "virtualMachineConfiguration": {
                "containerConfiguration": {
                    "containerImageNames": ["nginx", "python:3.9-alpine"],
                    "containerRegistries": {
                        "password": "myPassword",
                        "registryServer": "myContainerRegistry.azurecr.io",
                        "username": "myUserName",
                    },
                    "type": "DockerCompatible",
                },
            }
        },
        "resource_type": "Microsoft.Batch/batchAccounts/pools",
    }
    graph = DiGraph()
    graph.add_node(1, **resource)

    # when
    azure_provider = AzureTerraformProvider(graph_connector=graph)
    images = azure_provider.extract_images_from_resources()

    # then
    assert images == [
        Image(file_path="/batch.bicep", name="nginx", start_line=1, end_line=26),
        Image(file_path="/batch.bicep", name="python:3.9-alpine", start_line=1, end_line=26),
    ]


def test_extract_images_from_resources_with_no_image():
    # given
    resource = {
        "file_path_": "/batch.bicep",
        "__end_line__": 26,
        "__start_line__": 1,
        "properties": {
            "virtualMachineConfiguration": {
                "containerConfiguration": {
                    "containerImageNames": [],
                    "containerRegistries": {
                        "password": "myPassword",
                        "registryServer": "myContainerRegistry.azurecr.io",
                        "username": "myUserName",
                    },
                    "type": "DockerCompatible",
                },
            }
        },
        "resource_type": "Microsoft.Batch/batchAccounts/pools",
    }
    graph = DiGraph()
    graph.add_node(1, **resource)

    # when
    azure_provider = AzureTerraformProvider(graph_connector=graph)
    images = azure_provider.extract_images_from_resources()

    # then
    assert not images
