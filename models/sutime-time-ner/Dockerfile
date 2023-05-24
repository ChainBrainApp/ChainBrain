FROM ubuntu:latest

RUN apt-get update
RUN apt install -y default-jdk

RUN apt install -y python3 pip

RUN pip install notebook
RUN pip install sutime

RUN apt install -y wget tar
RUN wget https://apache.osuosl.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
RUN tar -xvf apache-maven-3.6.3-bin.tar.gz
RUN mv apache-maven-3.6.3 /opt/

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-arm64"
ENV PATH="$JAVA_HOME/bin:$PATH"

ENV M2_HOME='/opt/apache-maven-3.6.3'
ENV PATH="$M2_HOME/bin:$PATH"

COPY pom.xml .
RUN mvn dependency:copy-dependencies -DoutputDirectory=./jars -f pom.xml -P english

EXPOSE 8888