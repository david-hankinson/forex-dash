import pulumi
from pulumi_azure import core

# Create an Azure Resource Group
resource_group = core.ResourceGroup('my-resource-group')

# Export the name of the resource group
pulumi.export('resource_group_name', resource_group.name)
