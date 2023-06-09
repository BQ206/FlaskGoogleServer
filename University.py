import os 

from google.cloud.sql.connector import connector
import mysql.connector
import json
import sqlalchemy

INSTANCE_CONNECTION_NAME = f"lively-wave-340915:europe-west1:ca4006database" # i.e demo-project:us-central1:demo-instance
DB_USER = "admin"
DB_PASS = "food"
DB_NAME = "CA4006DB"

tst = {
  "type": "service_account",
  "project_id": "lively-wave-340915",
  "private_key_id": "dd9ed0f5626a32f292c74fa49d441ecd77f3d53f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCrjUk7ptQmBi+Z\nFlzd9fwLARze9rJa9WFMSld508X/xUMpgvy+TtoWcV0mxoU56+Am0kuqSEqLQ0Z8\nLUN+vk+EO09r+zl12sHfAG6Omy2jOwDbL2/Lp3pL/s3YBfftDcuAK+EU1KEEsVsG\nnoBEK+xwqq+lqDTUJYEfghZVkAPbDuMhf/aTyqoJyRkG8+WAOkI6CT9t18ByRJtr\nDAvZEVIF5zTN+exELIjmRNTrwuRdNCMNpE4XE/Z/EfR6dHUUmlrnwp0sJqiqxLIu\noCvmjTduRy7IUOxvwmAMInEA/urqSrmzPIoolFd4yYsIGtYHQk1aW84GADnROVrB\nSYJregbvAgMBAAECggEAAjpLylDfPojR4xmXbZ69ved4LkthGzpyQK5osBSVm5HU\nXR1k7FYw+At/MRpprxUrTT2G+kUmT5Phiv7ltOzhT+RgiQJAM3+Mx0RLPYax3FKC\nU92krMtAERGg11VRbCe1JbxbrbarmrsnRG/66OmMIqDBXrwfqY5zowvO8VMvn1iT\nbfgV2KN/qXqeZ5qTIbnMPQYHvxZRTXkPe5bDPWwX3eIioy3XMAwk+nRPamm6RZZO\nZ7J76PD+vx8Ks+aHlLYP2Op47CLemJrcSUv1xBh8u4SEGvdE9peR6Kfz2rYTd6ot\nibLcJjgJhWIvIzsoX1kn32V1/8fqQbRpL5TKw8DWoQKBgQDV6IeL4zJI/T9QSTwd\nvV/qeO47iFH23j0jHID3jIc6nvdjF5cZ/Hj/LqExrd7Tu+rxhav9S7d8AiknVfcT\n0EMr57lp7dIwRCIAb7y0EGH9KKHEP3Ao3FAay/LSRjFoSv58kmLu0bQb5mgMcWXs\nxte270CDAukgsraWkMMIxQw4oQKBgQDNTxV2KACUHZhxUu7i2dEtz6B0La4Qdb2J\nRlFMZCbDiixydsJMkPJlCDdQI42LX0hPgxHyUOaqF5wKfGW/Enz6PJHVIqzgYWs4\nL2BnltHrBDS49NC2rKB5aVgC0+tuB8ws+TIXBChugVG3m838CZMx0A5a+OxHEoJ/\nm5tClINFjwKBgGY1xMbX2cg8kgs34yzGt1UfUZ5KpfeS+52SWiFvGZKuMME9nWrC\nU8KDMmy9itKbYUjkuWi/zD3J/oYYMoZaJi6Ne/Acviln9ONGgOF9ToUb7CgMs/gi\nRXh4aV+GQMd3xiAaBoHc2/XU43TGnpBD9wEnUykGtAR2wH4zT64aEZvhAoGAMT10\nYkA500w90YAYdyPSfXA8hWCnTJ9Qc+n/eZjTizZKbrF47DAfUofj7D56piCWESvY\nVAt/JvA+pm0rYeYnP0TjnQCSAcabloAWWQHdGsaJdoqQvB8u5a+UQildX6hTGb4y\nez6uC8LMPIMLphUNznad2se0s18HGV/SnudLjJUCgYAFmuld61KDzwq07v9tH/lk\nkiAV/EQ0rZV4H1z2Ho9paw6nslp5lHuT/NV1sqogLDP3gvYEHBC0hJNZusC8xzDj\nGhkWAN81+5uGGwX19j9wtieA65ZdH6fYTu48MNAgac3eS8lOiL6cagFGvV1Un+Nq\n9xqkWrIXBwMgiuqH1NZy3A==\n-----END PRIVATE KEY-----\n",
  "client_email": "lively-wave-340915@appspot.gserviceaccount.com",
  "client_id": "107196161448967607355",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lively-wave-340915%40appspot.gserviceaccount.com"
}

json_object = json.dumps(tst, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./sample.json"


def ListResearchAccounts():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT Title, ID FROM ResearchAccount')
    information = c.fetchall()
    return information

def ListTransactions():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT amount,date,Reason,FundingAmount,ResearcherID FROM Transactions')
    information = c.fetchall()
    return information

def getResearcher(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT FullName FROM ResearcherAccounts WHERE ID = %s'
    val = (str(ID))
    c.execute(sql, val)
    information = c.fetchall()
    return information

def UniversityNotifications():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT date,budget,researcher,ID FROM UniversityNotifications ')
    information = c.fetchall()
    print(information)
    return information

def ResearchAccountInfo(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT Title, Budget, EndDate FROM ResearchAccount WHERE ID = %s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    return information

def UserInfo(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT FullName, Email FROM ResearcherAccounts WHERE ID = %s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    return information

def UserResearchAccounts(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT Title FROM ResearchAccount WHERE ResearcherID = %s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    return information

def AcknowledgeNotification(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = "DELETE FROM UniversityNotifications WHERE id = %s"
    val = (ID)
    c.execute(sql, val)
    conn.commit()
    conn.close()
    return information
