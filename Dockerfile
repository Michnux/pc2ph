FROM pdal/pdal:2.3

# RUN python -m pip install --upgrade pip
# RUN printenv && sleep 1m
# RUN pip3 -V && python -V && sleep 1m
# RUN ln python
RUN /opt/conda/bin/python -m pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org rasterio alteia
#RUN /opt/conda/bin/python -m pip install alteia
#RUN /opt/conda/bin/python -m pip install laspy

COPY script_dir /home/script_dir/

CMD ["python", "/home/script_dir/main.py"]
#CMD ["sleep", "1d"]
