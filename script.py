from azure.identity import DefaultAzureCredential
from azure.data.tables import LogsQueryClient
from datetime import timedelta

# Configuración de la conexión
credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

# Query KQL
query = """
let suspiciousAttempts =
    requests
    | where customDimensions.endpointName == "registerUserSPS" and isnotempty(tostring(customDimensions.Ip))
    | extend email_ = tostring(parse_json(tostring(parse_json(tostring(customDimensions.Request)).variables)).email)
    | summarize retries=count() by email_, bin(timestamp, 1d)
    | where retries > 1;

requests
| extend RequestId_ = tostring(customDimensions.RequestId)
| where customDimensions.endpointName == "registerUserSPS"
| extend Ip_ = tostring(customDimensions.Ip)
| extend Country_ = tostring(customDimensions.Country)
| extend Channel_ = tostring(customDimensions.Channel)
| extend email_ = tostring(parse_json(tostring(parse_json(tostring(customDimensions.Request)).variables)).email)
| extend AppVersion_ = tostring(customDimensions.AppVersion)
| extend Platform_ = tostring(customDimensions.Platform)
| extend crmId_ = tostring(parse_json(tostring(parse_json(tostring(parse_json(tostring(customDimensions.Response)).data)).registerUserSPS)).crmId)
| where isnotempty(crmId_)
 
| join kind=leftouter (suspiciousAttempts) on $left.email_ == $right.email_
 
| project timestamp, email_, crmId_, Ip_, Country_, Channel_, AppVersion_, Platform_, retries  
"""

# Ejecutar la consulta
response = client.query(workspace_id='defaultworkspace-e2b47bab-566d-4c2a-b432-883fbad1be10-neu', query=query, duration=timedelta(days=1))

# Procesar los resultados
for row in response.tables[0].rows:
    print(row)
