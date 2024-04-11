import pulumi
from pulumi_azure_native import containerregistry, resources

# Create an Azure Resource Group for forex-dash-infra
app_resource_group = resources.ResourceGroup('forex-dash-infra-app',
                                            location='uksouth',
                                            tags={
                                            'environment': 'production',  # Optionally, you can tag the resource group for organizational purposes
                                            })

registry_resource_group = resources.ResourceGroup('forex-dash-infra-registry',
                                            location='uksouth',
                                            tags={
                                            'environment': 'production',  # Optionally, you can tag the resource group for organizational purposes
                                            })
# Export the name of the resource groups
pulumi.export('resource_group_name', app_resource_group.name)
pulumi.export('resource_group_name', registry_resource_group.name)

# Create an Azure Container Registry
container_registry = containerregistry.Registry('forexDashInfraRegistry',
                                               resource_group_name=registry_resource_group.name,
                                                sku=containerregistry.SkuArgs(
                                                    # Choose between Basic, Standard, and Premium. Here we choose Basic.
                                                    name=containerregistry.SkuName.BASIC,
                                                ),
                                                # Enable admin user that allows for direct docker login
                                                admin_user_enabled=True,
                                            )

# Export the name of the container registry
pulumi.export('container_registry_name', container_registry.name)


