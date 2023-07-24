FROM ubuntu:latest

RUN apt-get update
RUN apt install -y default-jdk

RUN apt install -y python3 pip

RUN pip install Flask
RUN pip install notebook
RUN pip install sutime

RUN apt install -y wget tar
RUN wget https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.6.3/apache-maven-3.6.3-bin.tar.gz
RUN tar -xvf apache-maven-3.6.3-bin.tar.gz
RUN mv apache-maven-3.6.3 /opt/

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-arm64"
ENV PATH="$JAVA_HOME/bin:$PATH"

ENV M2_HOME='/opt/apache-maven-3.6.3'
ENV PATH="$M2_HOME/bin:$PATH"

COPY pom.xml .
RUN mvn dependency:copy-dependencies -DoutputDirectory=./jars -f pom.xml -P english

COPY routes.py .

EXPOSE 5001
ENV FLASK_APP=routes.py
ENV PORT=5001
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p 5001"]