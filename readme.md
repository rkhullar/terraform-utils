## Terraform Utils

### Notes
``` sh
docker run -d --name sonarqube -p 9000:9000 sonarqube
nosetests --with-xunit --with-coverage --cover-xml
sonar-scanner -D project.settings=cicd/sonar-project.properties
```
