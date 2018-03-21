FROM sd2e/python3:ubuntu17

RUN apt-get update
RUN apt-get -y install libxslt1-dev

RUN git clone https://github.com/SD2E/xplan_to_sbol

COPY xplan_to_sbol /xplan_to_sbol

# custom wheel for python 3.6
RUN pip3 install https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp36-none-any.whl?raw=true

# returns a non-zero exit code looking for a windows dependency
RUN cd /xplan_to_sbol && python3 setup.py install || true

RUN cd /xplan_to_sbol && python3 -m tests.SBOLTestSuite