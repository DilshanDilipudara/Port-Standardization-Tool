import re
import gitlab
from jira import JIRA

jira_server = {'server': 'https://dilshandilip.atlassian.net'}
jira_token = "<token>"
email = '<gmail>'

gl = gitlab.Gitlab(url='', private_token='')

jira = JIRA(jira_server, basic_auth=(email, jira_token))
projects = jira.projects()
standard_ports = {8080, 6060, 5050}
gitlab_group_ID = 10

# print(projects)

def create_issue(project_key, project_name, service_port):
    try:
        new_issue = jira.create_issue(project=str(project_key),
                                      summary=project_name + "'s port standardization",
                                      # description="The application port for " + project_name + "service needs to be standardized from " + service_port + " to 8080. ",
                                      description=r"""
                                                    1. Standardize Port
                                                    
                                                        The %s service currently uses port %s.
                                                        This ticket is for standardize the port to 8080 from %s, for consistency across services.
                                                    
                                                    Please refer the confluence page below : 
                                                        
                                                    
                                                    
                                                    2. Standardized Health Check Endpoints
                                                        
                                                            Readiness: /health/ready - Indicates if the service is ready to handle traffic.
                                                            Liveness: /health/live - Verifies if the service is alive and running.
                                                            Startup: /health/start - Provides an endpoint to signal successful service startup.
                                                    """ % (project_name, service_port, service_port),
                                      issuetype={'name': 'Task'})
        # Add labels to the created issue
        new_issue.update(fields={"labels": ["CICD", "TechDebt"]})
        print(f"New issue created: {new_issue.key}")
        # write the ticket ID in a file
        with open("jira_ticket.txt", "a") as file:
            file.write(new_issue.key + "\n")
    except Exception as e:
        print(e)


def jira_port(group_name, project_name, container_ports):
    c_ports = ", ".join(str(x) for x in container_ports)
    for project_key in projects:
        # core services
        if group_name == 'core-services' and 'CORE' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # passenger-services
        if group_name == 'passenger-services' and 'PASSENGER' == str(project_key):
            print(project_name, group.name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # driver-services
        if group_name == 'driver-services' and 'DRIVER' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # merchant-services
        if group_name == 'merchant-services' and 'MP' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # delivery-services
        if group_name == 'delivery-services' and 'DELIVERY' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # ride-services
        if group_name == 'ride-services' and 'PASSENGER' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # crm-services
        if group_name == 'crm-services' and 'CRM' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # portals-platform
        if group_name == 'portals-platform' and 'MP' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)
        # finance-services
        if group_name == 'finance-services' and 'FINANCE' == str(project_key):
            print(project_name, group_name, c_ports, str(project_key))
            create_issue(str(project_key), project.name, c_ports)


cicd_v2_group = gl.groups.get(gitlab_group_ID, lazy=True)
for group in cicd_v2_group.subgroups.list():
    for project in gl.groups.get(group.id, lazy=True).projects.list(get_all=True):
        try:
            file = gl.projects.get(project.id).files.raw(file_path='dev/k8s/deployment.yaml', ref='master')
            str_file = file.decode("utf-8")
            pattern = r'containerPort: (\d+)'
            matches = re.findall(pattern, str_file)
            container_ports = [int(port) for port in matches]
            # check port is not 8080
            if container_ports[0] != 8080 and len(container_ports) == 1:
                jira_port(group.name, project.name, container_ports)
            # check port is not 8080, 6060, 5050
            elif any(port not in standard_ports for port in container_ports):
                jira_port(group.name, project.name, container_ports)

        except Exception as e:
            print(project.name, e)
