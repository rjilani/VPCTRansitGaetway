import boto3
from util.json_utils import JsonUtil
from util.log_utils import setup_logs
import logging

setup_logs()
jsonutil = JsonUtil(logging.getLogger())
session = boto3.Session(
    profile_name='aws_source_admin',
    region_name='us-east-1'
)

ec2client = session.client('ec2')

ramclient = session.client('ram')

sessionorg = boto3.Session(
    profile_name='orguser_admin',
    region_name='us-east-1'
)

orgclient = sessionorg.client('ram')


# create transit gateway
def createtgateway(keyname, keyvalue, dryrun=False):
    logging.info("creating transit gateway")
    response = ec2client.create_transit_gateway(Description='this is a test to create transit gateway via boto3',
                                                Options={
                                                    'AutoAcceptSharedAttachments': 'enable'
                                                },
                                                TagSpecifications=[
                                                    {
                                                        'ResourceType': 'transit-gateway',
                                                        'Tags': [
                                                            {
                                                                'Key': keyname,
                                                                'Value': keyvalue
                                                            },
                                                        ]
                                                    },
                                                ],
                                                DryRun=dryrun)

    p_response = jsonutil.pretty_json(response)
    print(p_response)
    jsonutil.write_json_file("./orgdata/tgw.json", p_response)
    return response


# Describe the attributes for transit gateway
def describetransitgateway(tgatewayid, output=True, dryrun=False):
    logging.info("describing transit gateway")
    response = ec2client.describe_transit_gateways(
        TransitGatewayIds=[
            tgatewayid,
        ], DryRun=dryrun)

    p_response = jsonutil.pretty_json(response)
    if output:
        print(p_response)
    jsonutil.write_json_file("./orgdata/tgw_describe.json", p_response)
    return response

# Delete transit gateway
def deletetransitgateway(tgatewayid,  dryrun=False):
    try:
        logging.info("deleting transit gateway")
        response = ec2client.delete_transit_gateway(TransitGatewayId=tgatewayid,
                                                DryRun=dryrun)
        p_response = jsonutil.pretty_json(response)
        print(p_response)
        jsonutil.write_json_file("./orgdata/tgw_delete.json", p_response)
        return response

    except Exception as ex:
         print(str(ex))

# create resource share
def createresourceshare(name, resource_arns, principals):
    logging.info("creating resource share")
    response = ramclient.create_resource_share(
        name=name,
        resourceArns=resource_arns,
        principals=principals,
        tags=[
            {
                'key': 'Name',
                'value': 'Rashid Transit gateway share'
            },
        ],
        allowExternalPrincipals=True)

    p_response = jsonutil.pretty_json(response)
    print(p_response)
    jsonutil.write_json_file("./orgdata/tgw_shared.json", p_response)
    return response

# Get resource share invitation url
def getresourceshareinvitatons(resourcesharearns):
    logging.info("getting resource share invitations")
    response = orgclient.get_resource_share_invitations(

        resourceShareArns=resourcesharearns
    )

    p_response = jsonutil.pretty_json(response)
    print(p_response)
    jsonutil.write_json_file("./orgdata/tgw_resourceshareinvitation.json", p_response)
    return response

# accepts resource share invitations
def acceptresourceshare(resourceshareinvitationarn):
    logging.info("Accepting resource share invitation")
    try:
        response = orgclient.accept_resource_share_invitation(resourceShareInvitationArn=resourceshareinvitationarn)
        p_response = jsonutil.pretty_json(response)
        print(p_response)
        jsonutil.write_json_file("./orgdata/tgw_acceptinvitation.json", p_response)
        return response
    except Exception as ex:
        print(str(ex))

# creates attachement to VPC
def createattachments(gatewayid, vpcid, subnetids, dryrun=False):
    logging.info("Creating attachements")
    response = ec2client.create_transit_gateway_vpc_attachment(TransitGatewayId=gatewayid,
                                                               VpcId=vpcid,
                                                               SubnetIds=subnetids,
                                                               DryRun=dryrun)
    p_response = jsonutil.pretty_json(response)
    print(p_response)
    filename = 'tgw_attachments' + vpcid + '.json'
    jsonutil.write_json_file("./orgdata/" + filename , p_response)
    return response
