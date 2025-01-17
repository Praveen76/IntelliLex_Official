# pull python base image
FROM python:3.10

# specify working directory
WORKDIR /intlx_model_api

# copy in requirements and your wheel
ADD /intlx_model_api/requirements.txt .
ADD /intlx_model_api/*.whl .

# update pip
RUN pip install --upgrade pip

# install dependencies from requirements
RUN pip install -r requirements.txt

# install your local intlx_model wheel
RUN pip install *.whl

# remove the wheel after installing
RUN rm -f *.whl

# copy application code
ADD /intlx_model_api/app/* ./app/

EXPOSE 80
CMD ["python", "-u", "app/main.py"]
