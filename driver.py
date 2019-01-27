import time
import tgateway


def create_gateway():
    tgw_data_create = tgateway.createtgateway('Name', 'TGW01262019')
    transit_gateway = tgw_data_create['TransitGateway']
    tarnsitgateway_state = transit_gateway['State']
    tarnsitgateway_tags = transit_gateway['Tags'][0]
    tarnsitgateway_transitGatewayArn = transit_gateway['TransitGatewayArn']
    tarnsitgateway_transitGatewayId = transit_gateway['TransitGatewayId']
    tarnsitgateway_name = tarnsitgateway_tags['Value']
    print(tarnsitgateway_state)
    print(tarnsitgateway_transitGatewayArn)
    print(tarnsitgateway_transitGatewayId)
    print(tarnsitgateway_name)
    tgw_data_describe = tgateway.describetransitgateway(tarnsitgateway_transitGatewayId)
    tgateway_sate = tgw_data_describe['TransitGateways'][0]['State']
    # print (tgateway_sate )
    while not tgateway_sate == 'available':
        print('..... Transit gaeway is in ' + tgateway_sate + ' state  .....')
        print('..... Waiting for Transit gateway to be in available state...')
        time.sleep(40)
        tgw_data_describe = tgateway.describetransitgateway(tarnsitgateway_transitGatewayId, output=False)
        tgateway_sate = tgw_data_describe['TransitGateways'][0]['State']
    print(tgateway_sate)
    if tgateway_sate == 'available':
        transitgateway_resourceshare = tgateway.createresourceshare(name=tarnsitgateway_name,
                                                                    resource_arns=[tarnsitgateway_transitGatewayArn],
                                                                    principals=['000000000000']) #shared to account id
        transitgateway_resourceShareArn = transitgateway_resourceshare['resourceShare']['resourceShareArn']
        print(transitgateway_resourceShareArn)
        time.sleep(30)

        transitgateway_getresourceShareInvitationArn = tgateway.getresourceshareinvitatons(
            resourcesharearns=[transitgateway_resourceShareArn])
        transitgateway_resourceShareInvitationArn = \
        transitgateway_getresourceShareInvitationArn['resourceShareInvitations'][0]['resourceShareInvitationArn']
        print(transitgateway_resourceShareInvitationArn)
        time.sleep(30)

        tgateway.acceptresourceshare(resourceshareinvitationarn=transitgateway_resourceShareInvitationArn)

        time.sleep(10)
        tgateway.createattachments(tarnsitgateway_transitGatewayId, 'vpc-ID',
                                   ['subnet-IDS'])
        time.sleep(10)
        tgateway.createattachments(tarnsitgateway_transitGatewayId, 'vpc-ID',
                                   ['subnet-IDS'])




def delete_tgateay():
    tgw_data_delete = tgateway.deletetransitgateway('tgw-000000000000')
    print(tgw_data_delete)

# create_gateway()
delete_tgateay()