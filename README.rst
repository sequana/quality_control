
.. image:: https://badge.fury.io/py/sequana-quality-control.svg
     :target: https://pypi.python.org/pypi/sequana_quality_control

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/quality_control/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/quality_control/actions/workflows    


This pipeline is not maintained anymore but should be functional. It is a short-read quality control pipeline
from the `Sequana <https://sequana.readthedocs.org>`_ project. We would recommend to use the fastqc, demultiplex,
and multitax pipelines instead.

:Overview: A quality control pipeline for illumina data set. This pipeline removes contaminants (e.g. Phix), performs fastqc, adapter cleaning and trimming and checks for contaminants
:Input: Raw fastq files
:Output: Cleaned fastQ files, remove phix and adapters + taxonomy
:Status: production. **not maintained**. Please use sequana_fastqc and sequana_multitax pipeline instead
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_quality_control


Usage
~~~~~

::

    sequana_quality_control --help
    sequana_quality_control --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd quality_control
    sh quality_control.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s quality_control.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- fastqc
- bwa
- kraken2 (optional)
- krona (optional)
- sambamba
- samtools
- pigz
- cutadapt [or atropos]

.. image:: https://raw.githubusercontent.com/sequana/quality_control/master/sequana_pipelines/quality_control/dag.png


Details
~~~~~~~

This pipeline runs **quality_control** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_quality_control/master/sequana_pipelines/quality_control/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

ChangeLog
~~~~~~~~~


========= ====================================================================
Version   Description
========= ====================================================================
0.10.0    * add missing MANIFEST 
0.9.0     * remove design_file for cutadapt to reflect changes in
            sequana 0.12.0 
          * update kraken rules to use a kraken2 version
          * Update to use new sequana framework (0.12)
          * added CI action
0.8.4     * fix the onsuccess section to reflect changes in sequana 0.9.3
0.8.3     * fix cleaning output files
0.8.2     * fix typo in parameter (-skip-phix-removal --> --skip-phix-removal)
          * implement hiearchical kraken analysis. Required major updates of
            the sequana kraken rules + general fixes in sequana
0.8.1     uses more sequana tools to handle the options
========= ====================================================================
