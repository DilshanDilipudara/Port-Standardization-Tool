# Port Standardization Tool

This script is designed to automate the process of standardizing ports for various services within a project managed through Jira. It identifies services whose ports need to be standardized and creates corresponding Jira issues to track and manage this standardization process.


**How to Use**

Setup Jira Configuration: Ensure that your Jira instance is properly configured and accessible to the script.

Install Required Packages: Make sure you have the necessary Python packages installed. This script relies on the jira library.

Configure Project Groups: Modify the script to specify the project groups and their corresponding keys within your Jira instance. This is essential for the script to identify projects and create issues accordingly.

Run the Script: Execute the script in your Python environment. It will scan through the specified projects and their Kubernetes deployment files to identify non-standard ports.

Review Created Issues: After running the script, check your Jira instance for newly created issues related to port standardization. These issues will provide details about the service, its current port, and the proposed standardized port.


**Main Execution**

The main execution of the script involves iterating through project groups and their associated projects. It extracts container ports from Kubernetes deployment files and checks if port standardization is required. If non-standard ports are found, Jira issues are created using the create_issue function.









