# Use the OpenVINO Model Server as base image
FROM openvino/model_server:2023.3

# Copy models from your local machine to the Docker image
COPY ./openvino/models /models
COPY ./openvino/config.json /opt/ml/config.json

EXPOSE 8201

CMD ["--config_path", "/opt/ml/config.json", "--port", "8001", "--rest_port", "8002"]

# docker run --rm -v /home/luiz/repositories/Youtube-Newsletter/services/openvino/models:/models -v /home/luiz/repositories/Youtube-Newsletter/services/openvino/config.json:/opt/ml/config.json -p 8301:8001 ovserver